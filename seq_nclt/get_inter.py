from shapely.geometry import MultiPoint, LineString
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from scipy.spatial import KDTree
from scipy.spatial import distance
from IPython import embed

#avg_whole map

class sequence:
    def __init__(self) -> None:
        self.trajectory = None
        self.trajectory_id = None
        self.splat_file = None
        self.endpoint = None

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
x_2 = gt2[1:, 1]
y_2 = gt2[1:, 2]
trajectory2 = [(x1,y1) for x1,y1 in zip(x_2,y_2)]

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
# plt.figure()
# fig = plt.figure(figsize=(20, 20))
# plt.scatter(y_1, x_1, linewidth=0)    # Note Z points down
# plt.scatter(y_2, x_2, linewidth=0)    # Note Z points down
# plt.scatter(inter_y, inter_x, linewidth=0)    # Note Z points down
# plt.axis('equal')
# plt.title('Ground Truth Position of Nodes in SLAM Graph')
# plt.xlabel('East (m)')
# plt.ylabel('North (m)')
# plt.show()


intersection_dict={}

# Create a graph
G = nx.MultiGraph()
trajectories = [trajectory1,trajectory2]
for idx,i in enumerate(trajectories):
    kdtree = KDTree(i)
    new_intersection = {}
    for point in inter:
        new_intersection[find_closest_coordinate_kd_tree(point, kdtree, i)] = point
    tmp_sector=[i[0]]
    last_node = None
    for point_idx, point in enumerate(i[1:]):
        # print(point)
        if point in new_intersection.keys() or point_idx==len(i)-2:
            tmp_sector.append(point)
            if tmp_sector[0] in new_intersection.keys():
                s_p = new_intersection[tmp_sector[0]]
            else:
                s_p = tmp_sector[0]
            if point_idx==len(i)-2:
                e_p = point
            else:
                e_p = new_intersection[point]
            new_node = sequence()
            new_node.trajectory=tmp_sector
            new_node.trajectory_id=idx
            new_node.endpoint = tuple(sorted([s_p,e_p]))
            G.add_node(new_node)
            if s_p not in intersection_dict.keys():
                intersection_dict[s_p] = [new_node]
            else:
                intersection_dict[s_p].append(new_node)
            if e_p not in intersection_dict.keys():
                intersection_dict[e_p] = [new_node]
            else:
                intersection_dict[e_p].append(new_node)
            # if last_node!=None:
            #     G.add_edge(last_node, new_node)
            # print(tuple(sorted([s_p,e_p])))
            last_node = new_node
            tmp_sector = [e_p]
        else:
            tmp_sector.append(point)
        
for nodes in intersection_dict.values():
    for idx in range(len(nodes)):
        for idx_2 in range(idx+1, len(nodes)):
            if nodes[idx].endpoint == nodes[idx_2].endpoint:
                G.add_edge(nodes[idx], nodes[idx_2])            
            G.add_edge(nodes[idx], nodes[idx_2])
print(len(G.nodes()))
print(len([node for node, degree in G.degree() if degree == 2]))
# for node, degree in G.degree():
#     if degree==2:
#         print(node)

# Visualization
# pos = nx.spring_layout(G)  # Layout for the visualization
# labels = {node: str(node) for node in G.nodes()}  # Node labels
node_colors = [node.trajectory_id for node in G.nodes]
# nx.draw(G, node_size=1, node_color=node_colors)
pos = nx.spring_layout(G)

nx.draw(G, pos=pos, node_size=5, node_color=node_colors, width=1)
plt.savefig('plot.png')
