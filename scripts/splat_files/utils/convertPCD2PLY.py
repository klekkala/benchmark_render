#!/usr/bin/env python3

import argparse
import numpy as np

try:
    import open3d as o3d  # Make sure open3d is installed (pip install open3d)
except ImportError:
    print("Open3D is required for reading PCD files. Please install via 'pip install open3d'")
    exit(1)

def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert a PCD file into a minimal COLMAP points3D.txt format."
    )
    parser.add_argument("--input", type=str, required=True,
                        help="Path to the input .pcd file")
    parser.add_argument("--output", type=str, default="points3D.txt",
                        help="Path to the output points3D.txt file")
    return parser.parse_args()

def main():
    args = parse_args()

    # 1) Load the PCD using Open3D
    pcd = o3d.io.read_point_cloud(args.input)
    points = np.asarray(pcd.points)

    # 2) If the point cloud has colors, convert them to [0..255]. Otherwise default to zeros.
    #    Open3D stores colors in [0.0..1.0], so we multiply by 255.
    if pcd.colors:  # check if non-empty
        colors = (np.asarray(pcd.colors) * 255).astype(int)
    else:
        colors = np.zeros((points.shape[0], 3), dtype=int)

    # 3) Write COLMAP points3D file
    with open(args.output, 'w') as f:
        for i, (xyz, rgb) in enumerate(zip(points, colors), start=1):
            x, y, z = xyz
            r, g, b = rgb
            # ID, x, y, z, r, g, b, error=0.0, track_length=0
            line = f"{i} {x:.6f} {y:.6f} {z:.6f} {r} {g} {b} 0.0 0\n"
            f.write(line)

    print(f"Finished writing {args.output} with {len(points)} points.")

if __name__ == "__main__":
    main()
