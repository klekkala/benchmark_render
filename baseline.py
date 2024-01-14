import subprocess
import sys
from argparse import ArgumentParser, Namespace


import GPUtil
from threading import Thread
import time

class Monitor(Thread):
    def __init__(self, delay):
        super(Monitor, self).__init__()
        self.stopped = False
        self.delay = delay
        self.start()

    def run(self):
        while not self.stopped:
            GPUtil.showUtilization(True)
            time.sleep(self.delay)

    def stop(self):
        self.stopped = True
        
monitor = Monitor(0.1)

parser = ArgumentParser(description="Training script parameters")
parser.add_argument("--quiet", action="store_true")
args = parser.parse_args(sys.argv[1:])
subprocess.call(f"python test.py {args.quiet}", shell=True)
monitor.stop()
