from shapely.geometry import MultiPoint, LineString
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from scipy.spatial import KDTree
from scipy.spatial import distance
from IPython import embed
import random
#avg_whole map

class sequence:
    def __init__(self) -> None:
        self.trajectory = []
        self.trajectory_id = []
        self.splat_file = []
        self.endpoint = []

    def get_similarity(self):
        #TO BE DONE
        return 0

    def get_intersection(self,seq):
        Y = cdist(self.trajectory[0], seq)
        if np.min(Y)<0.1:
            return True
    

def detect_self_intersection(trajectory, trajectory2):
    line = LineString(trajectory)
    line2 = LineString(trajectory2)

    intersection = line.intersection(line2)
    return intersection

def find_closest_coordinate_kd_tree(target_coord, kdtree, coordinate_list):
    _, index = kdtree.query(target_coord)
    closest_coordinate = coordinate_list[index]

    return closest_coordinate

date = '2012-01-08'
date2= '2012-01-15'
gt = np.loadtxt('./ground_truth/groundtruth_%s.csv' % (date), delimiter = ",")
gt2 = np.loadtxt('./ground_truth/groundtruth_%s.csv' % (date2), delimiter = ",")

x_1 = gt[1:, 1]
y_1 = gt[1:, 2]
trajectory1 = [(x1,y1) for x1,y1 in zip(x_1,y_1)]
coor = [(x1,y1) for x1,y1 in zip(x_1,y_1)]
simplifed = [(x,y) for idx,(x,y) in enumerate(coor) if idx%50==0]
x_1 = [i[0] for i in simplifed]
y_1 = [i[1] for i in simplifed]


x_2 = gt2[1:, 1]
y_2 = gt2[1:, 2]
trajectory2 = [(x1,y1) for x1,y1 in zip(x_2,y_2)]
coor = [(x1,y1) for x1,y1 in zip(x_2,y_2)]
simplifed = [(x,y) for idx,(x,y) in enumerate(coor) if idx%50==0]

# simplifed = random.sample(coor, x_2.shape[0]//4)
x_2 = [i[0] for i in simplifed]
y_2 = [i[1] for i in simplifed]
# trajectory1 = [(0,0), (1,1), (2,1), (3,1), (4,0)]
# trajectory2 = [(0,1), (1,0), (2,0), (3,0), (4,1)]
# trajectory2 = [(5,1), (4,1), (3,0), (2,0), (1,0), (0,1)]

# print(trajectory1[0])
result = detect_self_intersection(trajectory1, trajectory2)
inter_x=[]
inter_y=[]
inter = []
for i in result.geoms:
    inter.append((i.x, i.y))
    inter_x.append(i.x)
    inter_y.append(i.y)


print(len(inter))
plt.figure()
fig = plt.figure(figsize=(20, 20))
plt.scatter(y_1, x_1, s=1, linewidth=0)    # Note Z points down
plt.scatter(y_2, x_2, s=1, linewidth=0)    # Note Z points down
plt.scatter(inter_y, inter_x, s=10, linewidth=0)    # Note Z points down
plt.axis('equal')
plt.title('Ground Truth Position of Nodes in SLAM Graph')
plt.xlabel('East (m)')
plt.ylabel('North (m)')
plt.savefig('Figure_3')
plt.show()



# # Create a graph
# G = nx.Graph()
# trajectories = [trajectory1,trajectory2]
# sectors = {}
# for idx,i in enumerate(trajectories):
#     kdtree = KDTree(i)
#     new_intersection = {}
#     for point in inter:
#         new_intersection[find_closest_coordinate_kd_tree(point, kdtree, i)] = point
#     tmp_sector=[i[0]]
#     last_node = None
#     for point_idx, point in enumerate(i[1:]):
#         # print(point)
#         if point in new_intersection.keys() or point_idx==len(i)-2:
#             tmp_sector.append(point)
#             if tmp_sector[0] in new_intersection.keys():
#                 s_p = new_intersection[tmp_sector[0]]
#             else:
#                 s_p = tmp_sector[0]
#             if point_idx==len(i)-2:
#                 e_p = point
#             else:
#                 e_p = new_intersection[point]
#             if tuple(sorted([s_p,e_p])) in sectors.keys():
#                 sectors[tuple(sorted([s_p, e_p]))].trajectory.append(tmp_sector)
#                 sectors[tuple(sorted([s_p, e_p]))].trajectory_id.append(idx)
#                 if last_node!=None:
#                     G.add_edge(last_node, sectors[tuple(sorted([s_p,e_p]))])
#                 last_node = sectors[tuple(sorted([s_p,e_p]))]
#             else:
#                 new_node = sequence()
#                 new_node.trajectory.append(tmp_sector)
#                 new_node.trajectory_id.append(idx)
#                 new_node.endpoint = tuple(sorted([s_p,e_p]))
#                 G.add_node(new_node)
#                 if last_node!=None:
#                     G.add_edge(last_node, new_node)
#                 sectors[tuple(sorted([s_p,e_p]))] = new_node
#                 # print(tuple(sorted([s_p,e_p])))
#                 last_node = new_node
#             tmp_sector = [e_p]
#         else:
#             tmp_sector.append(point)
        


# print(len(G.nodes()))
# print(len([node for node, degree in G.degree() if degree >= 3]))
# # Visualization
# # pos = nx.spring_layout(G)  # Layout for the visualization
# # labels = {node: str(node) for node in G.nodes()}  # Node labels

# nx.draw(G, node_size=7, node_color="skyblue")
# plt.show()
