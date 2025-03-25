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

## 3. Training Gaussian Splatting without colmap

1. Expected Files and Folder Structure

---

Gaussian Splatting expects three files in .bin format:

- cameras.bin
- images.bin
- points3D.bin

Your data folder should be structured like this:
2023_06_24/0/sector0/sparse/0/cameras.bin
2023_06_24/0/sector0/sparse/0/images.bin
2023_06_24/0/sector0/sparse/0/points3D.bin

Make sure all three .bin files are placed under sparse/0/ in the corresponding sector folder.

2. Converting Data to .bin Format

---

To get .bin files, you must first convert your data into .txt format:

Step 1: Convert surfaceMap.pcd (from Lego-loam) to .ply
python convertPCD2PLY.py

Step 2: Convert the resulting .ply to .txt
python convertPLY2TXT.py

These scripts help create a .txt file that can later be transformed into .bin.

3. Camera Intrinsics and camera.txt

---

The camera.txt file is hard-coded with the following values:

1 PINHOLE 1280 720 800 800 640 360

Feel free to adjust these intrinsics for optimization.

4. Generating images.txt

---

Step 1: Interpolate camera poses from the Lego-loam output
python interpolate_camera.py

Step 2: Convert these interpolated poses into the format required by Gaussian Splatting
python generate_images_cam.py

These scripts will produce images.txt, which is eventually converted to images.bin.

5. Converting .txt into .bin

---

Now we have three .txt file, we can type of following to convert the three .txt files into .bin files

```bash
colmap model_converter     --input_path ./TXT     --output_path ./BIN     --output_type BIN
```
