
#clip trajectory
#https://stackoverflow.com/questions/14631776/calculate-turning-points-pivot-points-in-trajectory-path

import numpy as np

import matplotlib.pyplot as plt

from rdp import rdp


date = '2012-01-08'
gt = np.loadtxt('./ground_truth/groundtruth_%s.csv' % (date), delimiter = ",")
x = gt[1:, 1]
y = gt[1:, 2]
trajectory = np.array([[x1,y1] for x1,y1 in zip(x,y)])
# trajectory = np.array([[0,0],[1,0],[1,1],[2,1],[3,1]])


def angle(directions):
    """Return the angle between vectors
    """
    vec2 = directions[1:]
    vec1 = directions[:-1]

    norm1 = np.sqrt((vec1 ** 2).sum(axis=1))
    norm2 = np.sqrt((vec2 ** 2).sum(axis=1))
    cos = (vec1 * vec2).sum(axis=1) / (norm1 * norm2)   
    return np.arccos(cos)


# Build simplified (approximated) trajectory
# using RDP algorithm.
simplified_trajectory = rdp(trajectory,50)
print(simplified_trajectory.shape)
sx, sy = simplified_trajectory.T

# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.plot(x, y, 'r--', label='trajectory')
# ax.plot(sx, sy, 'b-', label='simplified trajectory')
# ax.set_xlabel("X")
# ax.set_ylabel("Y")
# ax.legend(loc='best')
# plt.show()

# Define a minimum angle to treat change in direction
# as significant (valuable turning point).
min_angle = np.pi / 5.0

# Compute the direction vectors on the simplified_trajectory.
directions = np.diff(simplified_trajectory, axis=0)
theta = angle(directions)

# Select the index of the points with the greatest theta.
# Large theta is associated with greatest change in direction.
idx = np.where(theta > min_angle)[0] + 1

# Visualize valuable turning points on the simplified trjectory.
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(sx, sy, 'gx-', label='simplified trajectory')
ax.plot(x, y, 'r--', label='trajectory')
ax.plot(sx[idx], sy[idx], 'ro', markersize = 7, label='turning points')
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.legend(loc='best')


plt.show()








# from shapely.geometry import MultiPoint



# def detect_self_intersection(trajectory):
#     line = LineString(trajectory)
#     print(line)

#     # Check for self-intersection
#     if line.is_simple:  # No self-intersections
#         return None
#     else:
#         # Get the self-intersection point(s)
#         intersection = line.intersection(line)
#         return intersection.coords.xy

# # Example usage
# trajectory = [(0, 0), (1, 1), (2, 2), (1, 1), (0, 0)]

# result = detect_self_intersection(trajectory)
# print(result)
