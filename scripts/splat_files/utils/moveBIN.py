import os
import shutil

def move_files(src_folder, dst_folder):
    """
    Moves all files from src_folder to dst_folder.

    :param src_folder: Path to the source folder containing files to move
    :param dst_folder: Path to the target folder
    """
    # Ensure the destination folder exists
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)

    # Iterate through all entries in the source folder
    for entry in os.listdir(src_folder):
        src_path = os.path.join(src_folder, entry)

        # Only move if it is a file (not a directory, by default). 
        # Remove the check below if you want to move directories as well.
        if os.path.isfile(src_path):
            shutil.move(src_path, dst_folder)
            print(f"Moved {src_path} to {dst_folder}")

if __name__ == "__main__":
    source = "/lab/kiran/navisim/haopeng/data/colmap/BIN"
    dest = "/lab/tmpig23b/navisim/data/splat_files/2023-06-24/sparse/0"
    move_files(source, dest)