# benchmark
The baseline.py can record the train or render memory usage, GPU usage and GPU memory usage.

To run the baseline with train mode, simply use

```shell
python baseline.py --train
```

To run the baseline with render mode, simply use

```shell
python baseline.py
```

# gaussian splatting train
```shell
python ./gaussian-splatting/train.py -s ./gaussian-splatting/data/darkg --iterations 30000"
```
-s is the data
Then it will save point cloud file.

# gaussian splatting render
```shell
python ./gaussian-splatting/render.py -s ./gaussian-splatting/data/darkg  -m ./output/50aceb6b-6
```

-m means the saved point cloud file.
