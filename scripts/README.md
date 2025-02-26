# README

---

## 1. Running COLMAP

1. **Activate the Conda Environment**

   ```bash
   conda activate navisim_colmap
   ```

2. **Navigate to the COLMAP folder**

   ```bash
   cd ./gs_train/colmap
   ```

3. **(Option 1) Run COLMAP on a Specific Sector**

   ```bash
   python convert.py -s /lab/tmpig23b/navisim/data/gs_train_igpu23/2023_03_28/0/sector12/
   ```

4. **(Option 2) Run COLMAP on a Full Sequence**

   ```bash
   python run.py /lab/tmpig23b/navisim/data/gs_train_igpu23/2023_03_28/ 20
   ```

   20 indicates the number of concurrent threads to be used.

## 2. Training Gaussian Splatting

1. **Activate the Conda Environment**

   ```bash
   conda activate navisim
   ```

2. **Navigate to the Training folder**

   ```bash
   cd ./splat_files/3dgs_train
   ```

3. **(Option 1) Train on a Specific Sector**

   ```bash
   python train.py -s /lab/tmpig23b/navisim/data/gs_train_igpu23/2023_03_28/0/sector0
   ```

4. **(Option 2) Train on a Full Sequence**

   Note: Modifications to run_train.py are required.

   - data_path: the base directory containing your sector subfolders.
   - final_dest: the folder where all completed training outputs should be stored.
   - Adjust start_sector and end_sector as needed.

   ```bash
   python run_train.py
   ```
