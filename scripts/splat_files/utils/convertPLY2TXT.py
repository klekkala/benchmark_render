#!/usr/bin/env python3

import open3d as o3d
import numpy as np

# Input binary (or ASCII) PLY file:
ply_file = "/lab/kiran/navisim/haopeng/data/points3D.ply"
# Output points3D.txt path:
colmap_points3D_file = "/lab/kiran/navisim/haopeng/data/points3D.txt"

def ply_to_colmap_points3D(input_ply, output_txt):
    # 1. Read PLY (ASCII or binary) with Open3D
    pcd = o3d.io.read_point_cloud(input_ply)
    if not pcd.has_points():
        raise ValueError(f"No points were found in {input_ply}")
    
    # Extract points (Nx3) and colors (Nx3, each in [0.0..1.0])
    points = np.asarray(pcd.points)
    colors = np.asarray(pcd.colors)

    # If the PLY has no color, or they're all zeros, we can assign a default color
    if colors.size == 0 or not pcd.has_colors():
        colors = np.ones_like(points)  # all white or all black if you prefer
    else:
        # Open3D color values are floats in [0,1], so multiply by 255 for typical RGB
        colors = (colors * 255.0)
    
    # 2. Write out the points in COLMAP "points3D.txt" format:
    #    POINT3D_ID X Y Z R G B ERROR TRACK_LENGTH [ (IMAGE_ID, POINT2D_IDX), ... ]
    # Here we set ERROR = 0.0 and TRACK_LENGTH = 0, and no track data.
    with open(output_txt, 'w') as f:
        for idx, (p, c) in enumerate(zip(points, colors), start=1):
            x, y, z = p
            r, g, b = c
            error = 0.0
            track_length = 0
            # No (IMAGE_ID, POINT2D_IDX) references, so we just write the first 9 columns
            f.write(f"{idx} {x} {y} {z} {int(r)} {int(g)} {int(b)} {error} {track_length}\n")

    print(f"Done! Wrote {points.shape[0]} points to: {output_txt}")

if __name__ == "__main__":
    ply_to_colmap_points3D(ply_file, colmap_points3D_file)
