# README

---

## 1. Running COLMAP

1. **Navigate to the COLMAP folder**

   ```bash
   cd ./colmap
   ```

2. **(Option 1) Run COLMAP on a Specific Sector**

   ```bash
   python convert.py -s /lab/tmpig23b/navisim/data/gs_train_igpu23/2023_03_28/0/sector12/
   ```

3. **(Option 2) Run COLMAP on a Full Sequence**

   ```bash
   python run.py /lab/tmpig23b/navisim/data/gs_train_igpu23/2023_03_28/ 20
   ```

   20 indicates the number of concurrent threads to be used.

## 2. Training Gaussian Splatting

1. **Navigate to the Training folder**

   ```bash
   cd ./train
   ```

2. **(Option 1) Train on a Specific Sector**

   ```bash
   python train.py -s /lab/tmpig23b/navisim/data/gs_train_igpu23/2023_03_28/0/sector0
   ```

3. **(Option 2) Train on a Full Sequence**

   ```bash
   python run_train.py
   ```

   Note: Some modifications to run_train.py are required. You only need to specify the data_path and final_dest.
