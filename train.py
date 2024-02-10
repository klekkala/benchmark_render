import subprocess
import os
import sys

def generate_colmap(parent_folder):
    for folder_name in os.listdir(parent_folder):
        folder_path = os.path.join(parent_folder, folder_name)
        subprocess.call(f"python /lab/tmpig10c/kiran/nerf/GNerf/gaussian-splatting/train.py -s {folder_path} -m /home2/$1/$folder_name", shell=True)
        print(folder_path)

if __name__ == "__main__":
    parent_folder = sys.argv[1]
    generate_colmap(parent_folder)

