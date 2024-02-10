import os
import numpy as np
import pandas as pd
import plyvel
import argparse




def read_extrinsics_text(path):
    """
    Taken from https://github.com/colmap/colmap/blob/dev/scripts/python/read_write_model.py
    """
    images = {}
    with open(path, "r") as fid:
        while True:
            line = fid.readline()
            if not line:
                break
            line = line.strip()
            if len(line) > 0 and line[0] != "#":
                elems = line.split()
                image_id = int(elems[0])
                qvec = np.array(tuple(map(float, elems[1:5])))
                tvec = np.array(tuple(map(float, elems[5:8])))
                camera_id = int(elems[8])
                image_name = elems[9]
                elems = fid.readline().split()
                xys = np.column_stack([tuple(map(float, elems[0::3])),
                                       tuple(map(float, elems[1::3]))])
                point3D_ids = np.array(tuple(map(int, elems[2::3])))
                images[image_id] = Image(
                    id=image_id, qvec=qvec, tvec=tvec,
                    camera_id=camera_id, name=image_name,
                    xys=xys, point3D_ids=point3D_ids)
    return images


def generate_db(parent_folder):
    for folder_name in os.listdir(parent_folder):
        folder_path = os.path.join(parent_folder, folder_name)
        subprocess.call(f"python /lab/tmpig10c/kiran/nerf/GNerf/gaussian-splatting/convert.py -s {folder_path}", shell=True)
        print(folder_path)

#convert str to byte
def str2byte(s):
    s = s.encode()
    return s

#convert byte to str
def byte2str(b):
    b = b.decode()
    return b

def put2db(image_folder, pano_gps_dict, pano_head_dict, db):
    count=1
    for jpg in os.listdir(image_folder):
        print(count)
        count+=1
        if jpg in pano_gps_dict.keys():
            image_path = image_folder + '/' + jpg
            # image = cv2.imread(image_path)
            image = Image.open(image_path)
            width, _ = image.size
            headoff = pano_head_dict[jpg]
            if headoff<0:
                headoff = 360 + headoff
            dg = headoff / 360
            shift = int(width * dg)
            shifted_image = Image.new(image.mode, image.size)
            shifted_image.paste(image, (shift, 0))
            shifted_image.paste(image.crop((image.width - shift, 0, image.width, image.height)), (0, 0))
            shifted_image = np.array(shifted_image)
            shifted_image = cv2.cvtColor(shifted_image, cv2.COLOR_RGB2BGR)
            byte_image = cv2.imencode('.jpeg', shifted_image)[1]
            db.put(str2byte(pano_gps_dict[jpg]), byte_image)
        else:
            print(jpg)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str)
    parser.add_argument('--output', type=str)
    args = parser.parse_args()
    parent_folder = args.data

    db = plyvel.DB (f'{args.output}',create_if_missing =True, max_file_size = 1024*4096*16)
    #put k-v pairs
    put2db("data/pano_images", pano_gps_dict, pano_head_dict, db)
    print("successfully input all k-v pairs")
    #pull value
    cv2.imwrite('test.jpg',cv2.imdecode(np.frombuffer(db.get(str2byte('1.2904142071497517,-34.393438387352305')), np.uint8), -1))
