import os
import argparse
import numpy as np
import transforms3d as tf

# Function to convert Euler angles to quaternion and translation vector
def euler_to_quaternion_translation(roll, pitch, yaw, translation):
    rotation_matrix = tf.euler.euler2mat(roll, pitch, yaw, 'sxyz')
    # Negate the translation as done in your original code
    translation = -np.dot(rotation_matrix, translation)
    quaternion_result = tf.quaternions.mat2quat(rotation_matrix)
    return quaternion_result, translation

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, required=True)
    parser.add_argument('--odo', type=str, required=True)
    parser.add_argument('--target', type=str, required=True)
    args = parser.parse_args()

    img_path = args.data
    odo_path = args.odo
    target_path = args.target

    # Gather images
    imgs = sorted(
        f for f in os.listdir(img_path)
        if os.path.isfile(os.path.join(img_path, f))
    )

    # Build a dictionary from the odometry file
    odometry_dict = {}
    with open(odo_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip().split()
            # line[6] is presumably the filename
            odometry_dict[line[6]] = line

    curr = 0
    with open(target_path, 'w') as f:
        while True:
            # Check whether `curr` is within range
            if curr >= len(imgs):
                break

            img_name = imgs[curr]

            # If current image not in dictionary, skip it
            if img_name not in odometry_dict:
                curr += 1
                continue

            # Retrieve data from odometry dictionary
            temp = odometry_dict[img_name]

            # Convert strings to floats
            translation_vector = np.array([float(temp[0]), float(temp[1]), float(temp[2])])
            roll, pitch, yaw = float(temp[3]), float(temp[4]), float(temp[5])

            # Convert Euler angles to quaternion and get the adjusted translation
            quaternion_result, translation_result = euler_to_quaternion_translation(
                roll, pitch, yaw, translation_vector
            )

            # Write the output line to the target file
            f.write(
                f"{curr+1} "
                f"{quaternion_result[0]:.6f} {quaternion_result[1]:.6f} {quaternion_result[2]:.6f} {quaternion_result[3]:.6f} "
                f"{translation_result[0]:.6f} {translation_result[1]:.6f} {translation_result[2]:.6f} "
                f"1 {img_name}\n\n"
            )

            curr += 1

if __name__ == '__main__':
    main()

# python generate_images_cam.py \
#   --data /lab/tmpig23b/navisim/data/splat_files/2023-06-24/images \
#   --odo /lab/kiran/navisim/haopeng/data/interpolate_cam/odometry.txt \
#   --target /lab/kiran/navisim/haopeng/data/images.txt