import os
from argparse import ArgumentParser

parser = ArgumentParser("interval")

parser.add_argument("--end", default=12042, type=int)
parser.add_argument("--step", default=250, type=int)
parser.add_argument("--target_path", "-t", required=True, type=str)
#/home2/bag_dump/2023_06_29/session0
args = parser.parse_args()
end = args.end
step = args.step
start = step
with open(os.path.join(args.target_path, 'intervals.txt'), 'w') as file:
    for number in range(start, end + 1, step):
        file.write(str(number) + '\n')

