import os
import shutil
import subprocess

def run_training(base_path, final_dest, start_sector, end_sector):
    # output_base = "/lab/student/motion_model/haopeng/train/output"
    output_base = "./output"

    for sector in range(start_sector, end_sector + 1):
        sector_path = f"{base_path}/sector{sector}"
        cmd = ["python", "train.py", "-s", sector_path]

        # List of directories before running train.py
        before_dirs = set(os.listdir(output_base))

        print(f"Running command: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)  # This will block until train.py completes

        # List of directories after running train.py
        after_dirs = set(os.listdir(output_base))

        # Find the newly created folder by comparing before/after
        new_dirs = after_dirs - before_dirs
        if len(new_dirs) == 1:
            random_dir_name = new_dirs.pop()
            old_dir_path = os.path.join(output_base, random_dir_name)

            # Construct new directory name (e.g., 'sector0', 'sector1', etc.)
            new_dir_name = f"sector{sector}"
            new_dir_path = os.path.join(output_base, new_dir_name)

            # Rename the folder
            print(f"Renaming {old_dir_path} to {new_dir_path}")
            os.rename(old_dir_path, new_dir_path)

            # Move the folder to the final destination
            destination_path = os.path.join(final_dest, new_dir_name)
            print(f"Moving {new_dir_path} to {destination_path}")
            shutil.move(new_dir_path, final_dest)

        else:
            print(f"Warning: Expected exactly one new directory, found {len(new_dirs)}. "
                  "Skipping rename and move for sector {sector}.")

if __name__ == "__main__":
    data_path = "/lab/tmpig23b/navisim/data/gs_train_igpu23/2023_03_28/0"
    final_dest = "/lab/tmpig23b/navisim/data/gs_train_igpu23/test_training"

    run_training(data_path, final_dest, start_sector=0, end_sector=33)

# nohup python run_train.py &