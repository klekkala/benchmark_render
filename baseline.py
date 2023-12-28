import subprocess
import sys
from argparse import ArgumentParser, Namespace

import matplotlib.pyplot as plt
import GPUtil
from threading import Thread
import time
import psutil

gpuInfo=[]
memInfo=[]
gpuMemPer=[]
gpuMem=[]

class Monitor(Thread):
    def __init__(self, delay):
        super(Monitor, self).__init__()
        self.stopped = False
        self.delay = delay # Time between calls to GPUtil
        self.start()

    def run(self):
        while not self.stopped:
            GPUs = GPUtil.getGPUs()
            load = GPUs[0].load
            gpuMemPer.append(GPUs[0].memoryUtil)
            gpuMem.append(GPUs[0].memoryUsed)
            gpuInfo.append(load)
            memory_info = psutil.virtual_memory()
            memInfo.append(memory_info.percent/100)
            time.sleep(self.delay)

    def stop(self):
        self.stopped = True
        
# Instantiate monitor with a 10-second delay between updates
monitor = Monitor(1)

parser = ArgumentParser(description="Training script parameters")
parser.add_argument("--quiet", action="store_true")
parser.add_argument("--train", action="store_true")
args = parser.parse_args(sys.argv[1:])
# subprocess.call(f"python test.py {args.quiet}", shell=True)
if args.train:
    subprocess.call(f"python ./GNerf/gaussian-splatting/train.py -s ./GNerf/gaussian-splatting/data/darkg --iterations 60000", shell=True)
else:
    subprocess.call(f"python ./GNerf/gaussian-splatting/render.py -m ./output/50aceb6b-6", shell=True)

#if args.train:
#    subprocess.call(f"python ./GNerf/4d/4DGaussians/train.py -s ./GNerf/4d/4DGaussians/data/darkg --expname 'dynerf/darkg' --configs ./GNerf/4d/4DGaussians/arguments/dynerf/default.py", shell=True)
#else:
#    subprocess.call(f"python ./GNerf/4d/4DGaussians/render.py --model_path ./GNerf/4d/4DGaussians/output/darkg  --skip_test --configs ./GNerf/4d/4DGaussians/arguments/dynerf/default.py", shell=True)

monitor.stop()

x_values = range(1, len(gpuInfo) + 1)

plt.plot(x_values, gpuInfo, label='GPU Usage')
# plt.plot(x_values, memInfo, label='RAM')
# plt.plot(x_values, gpuMemPer, label='VRAM')

plt.xlabel('Time')
plt.ylabel('Percent')
plt.legend()
plt.savefig('4d GPU Usage.png')

plt.clf()

plt.plot(x_values, gpuMem)
plt.xlabel('Time')
plt.ylabel('GPU Memory Usage')
plt.legend()
plt.savefig('4d GPU Memory Usage.png')

print(sum(gpuInfo)/len(gpuInfo))
print(sum(memInfo)/len(memInfo))
print(sum(gpuMemPer)/len(gpuMemPer))
print(sum(gpuMem)/len(gpuMem))
