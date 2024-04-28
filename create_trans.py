import numpy as np
from argparse import ArgumentParser
import os, json
from os.path import join
import struct

# This Python script is based on the shell converter script provided in the MipNerF 360 repository.
parser = ArgumentParser()
parser.add_argument("--sector", "-s", required=True, type=str)
parser.add_argument("--odometry", "-o", required=True, type=str)
parser.add_argument("--sync", required=True, type=str)
args = parser.parse_args()


def qvec2rotmat(qvec):
    return np.array([
        [1 - 2 * qvec[2]**2 - 2 * qvec[3]**2,
         2 * qvec[1] * qvec[2] - 2 * qvec[0] * qvec[3],
         2 * qvec[3] * qvec[1] + 2 * qvec[0] * qvec[2]],
        [2 * qvec[1] * qvec[2] + 2 * qvec[0] * qvec[3],
         1 - 2 * qvec[1]**2 - 2 * qvec[3]**2,
         2 * qvec[2] * qvec[3] - 2 * qvec[0] * qvec[1]],
        [2 * qvec[3] * qvec[1] - 2 * qvec[0] * qvec[2],
         2 * qvec[2] * qvec[3] + 2 * qvec[0] * qvec[1],
         1 - 2 * qvec[1]**2 - 2 * qvec[2]**2]])

def read_next_bytes(fid, num_bytes, format_char_sequence, endian_character="<"):
    """Read and unpack the next bytes from a binary file.
    :param fid:
    :param num_bytes: Sum of combination of {2, 4, 8}, e.g. 2, 6, 16, 30, etc.
    :param format_char_sequence: List of {c, e, f, d, h, H, i, I, l, L, q, Q}.
    :param endian_character: Any of {@, =, <, >, !}
    :return: Tuple of read and unpacked values.
    """
    data = fid.read(num_bytes)
    return struct.unpack(endian_character + format_char_sequence, data)

def read_extrinsics_binary(path_to_model_file):
    """
    see: src/base/reconstruction.cc
        void Reconstruction::ReadImagesBinary(const std::string& path)
        void Reconstruction::WriteImagesBinary(const std::string& path)
    """
    images = {}
    with open(path_to_model_file, "rb") as fid:
        num_reg_images = read_next_bytes(fid, 8, "Q")[0]
        for _ in range(num_reg_images):
            binary_image_properties = read_next_bytes(
                fid, num_bytes=64, format_char_sequence="idddddddi")
            image_id = binary_image_properties[0]
            qvec = np.array(binary_image_properties[1:5])
            tvec = np.array(binary_image_properties[5:8])
            camera_id = binary_image_properties[8]
            image_name = ""
            current_char = read_next_bytes(fid, 1, "c")[0]
            while current_char != b"\x00":   # look for the ASCII 0 entry
                image_name += current_char.decode("utf-8")
                current_char = read_next_bytes(fid, 1, "c")[0]
            num_points2D = read_next_bytes(fid, num_bytes=8,
                                           format_char_sequence="Q")[0]
            x_y_id_s = read_next_bytes(fid, num_bytes=24*num_points2D,
                                       format_char_sequence="ddq"*num_points2D)
            qvec = qvec2rotmat(qvec)
            tvec = -np.dot(qvec.T, tvec)
            images[image_name] = tvec
    return images


# def tran(qvec, tvec):
#     rotation_matrix = tf.quaternions.quat2mat(qvec)
#     translation = -np.dot(rotation_matrix.T, tvec)
#     return translation

def find_closest_number(number, sorted_list):
    if not sorted_list:
        return None
    left = 0
    right = len(sorted_list) - 1
    while left <= right:
        mid = (left + right) // 2
        if sorted_list[mid] == number:
            return sorted_list[mid]
        elif sorted_list[mid] < number:
            left = mid + 1
        else:
            right = mid - 1
    if right < 0:
        return sorted_list[0]
    elif left >= len(sorted_list):
        return sorted_list[-1]
    else:
        if abs(sorted_list[right] - number) < abs(sorted_list[left] - number):
            return sorted_list[right]
        else:
            return sorted_list[left]


def kabsch(P, Q):
    """
    Computes the optimal translation and rotation matrices that minimize the 
    RMS deviation between two sets of points P and Q using Kabsch's algorithm.
    More here: https://en.wikipedia.org/wiki/Kabsch_algorithm
    Inspiration: https://github.com/charnley/rmsd
    
    inputs: P  N x 3 numpy matrix representing the coordinates of the points in P
            Q  N x 3 numpy matrix representing the coordinates of the points in Q
            
    return: A 4 x 3 matrix where the first 3 rows are the rotation and the last is translation
    """
    if (P.size == 0 or Q.size == 0):
        raise ValueError("Empty matrices sent to kabsch")
    centroid_P = np.mean(P, axis=0)
    centroid_Q = np.mean(Q, axis=0)
    P_centered = P - centroid_P                       # Center both matrices on centroid
    Q_centered = Q - centroid_Q
    H = P_centered.T.dot(Q_centered)                  # covariance matrix
    U, S, VT = np.linalg.svd(H)                        # SVD
    R = U.dot(VT).T                                    # calculate optimal rotation
    if np.linalg.det(R) < 0:                          # correct rotation matrix for             
        VT[2,:] *= -1                                  #  right-hand coordinate system
        R = U.dot(VT).T                          
    t = centroid_Q - R.dot(centroid_P)                # translation vector
    # right-cross matrix, shape(4,3)
    return np.vstack((R, t))


if not os.path.isdir(args.sector) and not os.path.exists(args.odometry) and not os.path.exists(args.sync):
    print('wrong input')
    exit(0)

right_x=[]
right_y=[]
right_z=[]
right_n=[]

if not os.path.exists(join(args.sector, 'sparse', '0', 'images.bin')):
    print(join(args.sector, 'sparse', '0', 'images.bin'))
    print('no images.bin')
    exit(0)
images = read_extrinsics_binary(join(args.sector, 'sparse', '0', 'images.bin'))

with open(args.sync, "r") as json_file:
    cams = json.load(json_file)

odo = {}
with open(args.odometry, "r") as f:
    for line in f:
        poses = line.strip().split(", ")
        odo[int(poses[6].replace('.', ''))] = np.array([float(poses[0]), float(poses[1]), float(poses[2])])

start = 9<<100
end = 0
for img_name in images.keys():
    if img_name[3] == '1':
        if int(img_name[5:-4]) < start:
            start = int(img_name[5:-4])
        if int(img_name[5:-4]) > end:
            end = int(img_name[5:-4])

odo_points = []
decimal_places = len(str(list(odo.keys())[0]))
o_start = int(str(start)[:decimal_places])
o_end = int(str(end)[:decimal_places])

time_dicts = []
rounded_file_names = []
for i in range(5):
    time_dict = {}
    tmp = []
    for cam_n, time in cams[i].items():
        tmp.append(int(str(time)[:decimal_places]))
        time_dict[tmp[-1]] = cam_n
    time_dicts.append(time_dict)
    rounded_file_names.append(tmp)
rounded_file_names = [sorted(i) for i in rounded_file_names]

cal_tra = []
real_tra = []

for key, value in odo.items():
    if key >= o_start and key <= o_end:
        need_cams = []
        for i in range(5):
            cam_t = find_closest_number(key, rounded_file_names[i])
            if time_dicts[i][cam_t] in images.keys():
                need_cams.append(time_dicts[i][cam_t])
            else:
                break
        if len(need_cams) == 5:
            real_tra.append(value)
            tmp = [0, 0, 0]
            for i in range(3):
                for q in range(5):
                    tmp[i] += images[need_cams[q]][i]
            tmp = [i/5 for i in tmp]
            cal_tra.append(np.array(tmp))

trans = kabsch(np.array(cal_tra), np.array(real_tra))
print(trans)
# print(np.dot(trans[:-1], np.array([-1.56651852,  0.04218873, -5.54782173]))+trans[-1])

