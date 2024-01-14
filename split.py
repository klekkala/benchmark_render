import os
import shutil

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--data', type=str)
parser.add_argument('--target', type=str)
parser.add_argument('--intervalfile', type=str)
parser.add_argument('--num', type=int, default = -1)
args = parser.parse_args()

def copy_file(source_path, destination_path):
    try:
        shutil.copy2(source_path, destination_path)
        print(f"File copied successfully from '{source_path}' to '{destination_path}'.")
    except FileNotFoundError:
        print(f"Error: The file '{source_path}' does not exist.")
    except PermissionError:
        print(f"Error: Permission denied. Unable to copy the file.")

img_path = args.data
target_path = args.target
if img_path[-1]!='/':
    img_path+='/'
if target_path[-1]!='/':
    target_path+='/'

if not os.path.exists(target_path):
    os.makedirs(target_path)

intervals=[]
with open(args.intervalfile, 'r') as file:
    lines = file.readlines()

    for line in lines:
        intervals.append(int(line.strip()))

count=0
tra=0
flag=0
while True:
    os.makedirs(target_path+'sector'+str(tra)+'/input')
    os.mkdir(target_path+'sector'+str(tra)+'/gt_dense')
    os.mkdir(target_path+'sector'+str(tra)+'/gt_annot')
    while True:
        for i in range(1,6):
            if not os.path.exists(f'{img_path}cam{i}_image_{count}.jpg'):
                flag=1
                break
            copy_file(f'{img_path}cam{i}_image_{count}.jpg', f'{target_path}sector{tra}/input/cam{i}_image_{count}.jpg')
        if flag==1:
            break
        count+=1
        if count in intervals:
            print(count)
            break
    if flag==1:
        break
    tra+=1
    if args.num==tra:
        break

