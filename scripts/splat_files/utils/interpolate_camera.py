import os
import numpy as np
from scipy.interpolate import interp1d
import transforms3d as tf
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--img_path', type=str, required=True)
    parser.add_argument('--output', type=str, required=True)
    parser.add_argument('--odo', type=str, required=True)
    args = parser.parse_args()

    ODOM_FILE = args.odo
    OUTFILE   = args.output

    # --- 1) Read image filenames and group them ---
    file_names = []
    name_dict = {}
    for fn in os.listdir(args.img_path):
        if fn.endswith(".jpg"):
            key = int(fn[5:-4])  # e.g., 'cam1_12345.jpg' -> 12345
            if key not in name_dict:
                name_dict[key] = []
                file_names.append(key)
            name_dict[key].append(fn)

    file_names.sort()

    # --- 2) Read odometry file (x, y, z, row, pitch, yaw, time) ---
    x_vals, y_vals, z_vals = [], [], []
    row_vals, pitch_vals, yaw_vals = [], [], []
    time_vals = []
    with open(ODOM_FILE, "r") as f:
        for line in f:
            # Suppose each line is something like: "z, y, x, row, pitch, yaw, time"
            # with ", " as the separator
            poses = line.strip().split(", ")
            x_vals.append(float(poses[2]))
            y_vals.append(float(poses[1]))
            z_vals.append(float(poses[0]))
            row_vals.append(float(poses[3]))
            pitch_vals.append(float(poses[4]))
            yaw_vals.append(float(poses[5]))
            # Last entry is time; remove '.' then convert to int
            time_vals.append(int(poses[6].replace('.', '')))

    # --- 3) Build interpolators for each dimension ---
    interpolator_x = interp1d(time_vals, x_vals)
    interpolator_y = interp1d(time_vals, y_vals)
    interpolator_z = interp1d(time_vals, z_vals)
    interpolator_row = interp1d(time_vals, row_vals)
    interpolator_pitch = interp1d(time_vals, pitch_vals)
    interpolator_yaw = interp1d(time_vals, yaw_vals)

    # Determine min/max allowed times from odometry
    t_min, t_max = min(time_vals), max(time_vals)

    # --- 4) Build (and clamp) interpolation_time from filenames ---
    decimal_places = len(str(time_vals[-1]))  # used to truncate the filename-based times
    rounded_times = []
    time_dict = {}  # map the truncated time back to the "true" file_names index

    for i in file_names:
        truncated_i = int(str(i)[:decimal_places])  # e.g., "1234567"[:7]
        rounded_times.append(truncated_i)
        time_dict[truncated_i] = i

    rounded_times.sort()
    interpolation_time = np.array(rounded_times)

    # Clamp interpolation_time so none are below t_min or above t_max
    valid_mask = (interpolation_time >= t_min) & (interpolation_time <= t_max)
    interpolation_time_clamped = interpolation_time[valid_mask]

    # --- 5) Identify "closest_pose" for each odometry time (as in your code) ---
    #        (This logic is the same as yours, but we only consider the clamped times.)
    closest_pose = []
    for i in range(len(time_vals)):
        tmp_diffs = [1e15 for _ in range(6)]
        res_names = ['' for _ in range(6)]
        for it_val in interpolation_time_clamped:
            # For each truncated time, get its actual file(s)
            # e.g. name_dict[ time_dict[it_val] ] might be multiple files
            fn_list = name_dict[ time_dict[it_val] ]
            for file_name in fn_list:
                cam_idx = int(file_name[3])  # 'cam1_xxxx.jpg' -> 1
                diff = abs(it_val - time_vals[i])
                if diff < tmp_diffs[cam_idx - 1]:
                    tmp_diffs[cam_idx - 1] = diff
                    res_names[cam_idx - 1] = file_name
        closest_pose.extend(res_names)

    # --- 6) Interpolate x, y, z, row, pitch, yaw at the clamped times ---
    interpolated_x     = interpolator_x(interpolation_time_clamped)
    interpolated_y     = interpolator_y(interpolation_time_clamped)
    interpolated_z     = interpolator_z(interpolation_time_clamped)
    interpolated_row   = interpolator_row(interpolation_time_clamped)
    interpolated_pitch = interpolator_pitch(interpolation_time_clamped)
    interpolated_yaw   = interpolator_yaw(interpolation_time_clamped)

    # --- 7) Define your camera-specific translation/rotation offsets ---
    translation = [
        [0.05004123414516961,  0.121650402733524,  -0.019],
        [-0.100232816459295,   0.0851840836344303, -0.019],
        [0.03102010381926821, -0.127830742621022,  -0.019],
        [-0.11198852150514299,-0.0690037437469328, -0.019],
        [0.13116,              -0.01,              -0.019]
    ]

    rotation = [
        [0,  2.82743338823082 - 3.14159265358979,  0],
        [0,  3.14159265358979 - 2.19911485751285,  0],
        [0,  0.314159265358991 - 3.14159265358979, 0],
        [0,  3.14159265358979 - 0.942477796076929,0],
        [0, -1.5707963267949,                     0]
    ]

    # --- 8) Write out the final odometry.txt ---
    os.makedirs(OUTFILE, exist_ok=True)
    output_path = os.path.join(OUTFILE, 'odometry.txt')
    with open(output_path, 'w') as f:
        # Loop through each clamped time index
        for i, t_val in enumerate(interpolation_time_clamped):
            # For each truncated time, retrieve the file(s)
            fn_list = name_dict[ time_dict[t_val] ]
            for file_name in fn_list:
                # Only write if it's in the "closest_pose"
                if file_name not in closest_pose:
                    continue
                cam = int(file_name[3])

                # Apply the offset translations and rotations
                x_out = interpolated_x[i] + translation[cam-1][0]
                y_out = interpolated_y[i] + translation[cam-1][2]
                z_out = interpolated_z[i] + translation[cam-1][1]
                row_out  = interpolated_row[i]   + rotation[cam-1][0]
                pitch_out= interpolated_pitch[i] + rotation[cam-1][1]
                yaw_out  = interpolated_yaw[i]   + rotation[cam-1][2]

                # Write one line per file
                f.write(f"{x_out:.6f} {y_out:.6f} {z_out:.6f} "
                        f"{row_out:.6f} {pitch_out:.6f} {yaw_out:.6f} "
                        f"{file_name}\n")

    print(f"Done. Wrote interpolations to {output_path}.")

if __name__ == "__main__":
    main()

# python interpolate_camera.py --img_path /lab/tmpig23b/navisim/data/splat_files/2023-06-24/images --output /lab/kiran/navisim/haopeng/data/interpolate_cam --odo /lab/kiran/navisim/haopeng/data/odometry.txt
