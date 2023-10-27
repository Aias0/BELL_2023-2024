import numpy as np
import math, random, Geometry3D
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

nodes = [[[0, 0, 0, 0, 0, 1, 0],
          [0, 0, 0, 1, 0, 0, 0],
          [0, 1, 0, 0, 1, 1, 0],
          [0, 0, 1, 1, 0, 0, 1],
          [1, 1, 0, 1, 0, 0, 1],
          [0, 0, 1, 0, 1, 0, 0],
          [0, 0, 0, 0, 1, 0, 1]],
         [[1, 1, 1, 1, 0, 1, 0],
          [1, 1, 1, 1, 0, 0, 0],
          [1, 1, 1, 0, 0, 1, 0],
          [1, 0, 1, 1, 0, 1, 0],
          [1, 1, 0, 1, 1, 0, 1],
          [0, 0, 0, 0, 1, 1, 1],
          [0, 0, 0, 0, 1, 0, 1]],
         [[1, 1, 0, 1, 1, 1, 0],
          [1, 1, 0, 0, 1, 1, 0],
          [0, 1, 0, 1, 1, 1, 0],
          [0, 0, 1, 0, 1, 0, 1],
          [1, 1, 0, 1, 0, 0, 1],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 1]],
         [[0, 0, 0, 0, 0, 1, 0],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 1, 0, 0, 1, 1, 0],
          [0, 0, 1, 0, 0, 0, 0],
          [1, 1, 0, 1, 0, 0, 1],
          [0, 0, 0, 0, 1, 0, 0],
          [0, 0, 0, 0, 1, 0, 0]],]
#nodes = [[[0 for i in range(len(nodes[0][0]))] for j in range(len(nodes[0]))] for k in range(len(nodes))]

def print2d(list):
    for i, r in enumerate(list):
        if i == 0:
            print(f'[{r}')
        elif i == len(list)-1:
            print(f' {r}]')
        else:
            print(f' {r}')
def print_3d(lst):
    for i, slice in enumerate(lst):
        print2d(slice)
        print()

def path_find_3d(start, end, nodes):
    # Define the surrounding nodes in 3D space
    surrounding_nodes = [
        (-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)
    ]

    def heuristic(node):
        return ((node[0] - end[0])**2+(node[1] - end[1])**2+(node[2] - end[2])**2)**0.5
        return abs(node[0] - end[0]) + abs(node[1] - end[1]) + abs(node[2] - end[2])

    def get_neighbors(node):
        neighbors = []
        for dx, dy, dz in surrounding_nodes:
            x, y, z = node[0] + dx, node[1] + dy, node[2] + dz
            if (
                0 <= x < len(nodes[0][0]) and
                0 <= y < len(nodes[0]) and
                0 <= z < len(nodes) and
                nodes[z][y][x] != 1
            ):
                neighbors.append((x, y, z))
        return neighbors

    open_set = [start]
    came_from = {}
    g_score = {(x, y, z): float('inf') for z, layer in enumerate(nodes) for y, row in enumerate(layer) for x, _ in enumerate(row)}
    g_score[start] = 0
    f_score = {(x, y, z): float('inf') for z, layer in enumerate(nodes) for y, row in enumerate(layer) for x, _ in enumerate(row)}
    f_score[start] = heuristic(start)

    while open_set:
        current = min(open_set, key=lambda node: f_score[node])

        if current == end:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            # Path cleanup
            opti_path = [path[0]]
            prev_node = None
            print(path)
            for i in range(len(path)):
                if i+1 > len(path)-1:
                    break
                for j in range(len(path[i+1])):
                    if abs(path[i+1][j] - path[i][j]) == 1:
                        k=i
                        while abs(path[k+1][j] - path[k][j]) == 1:
                            k+=1
                            if k+1 > len(path)-1:
                                break
                        opti_path.append(path[k])
                        break
            opti_path = [i for n, i in enumerate(opti_path) if i not in opti_path[:n]]

            return opti_path
        
        open_set.remove(current)
        for neighbor in get_neighbors(current):
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor)
                if neighbor not in open_set:
                    open_set.append(neighbor)

    print("No valid path found")
    return None

start = (0, 0, 0)
end = (0, 6, 3)
path = path_find_3d(start, end, nodes)
if path:
    print('test')
    print_3d(nodes)
    path_map = [[[' ' for i in range(len(nodes[0][0]))] for j in range(len(nodes[0]))] for k in range(len(nodes))]
    for x, y, z in path:
        path_map[z][y][x] = 'O'
    obstacle_list = [] 
    for i, h in enumerate(nodes):
        for j, r in enumerate(h):
            for k, node in enumerate(r):
                if node == 1:
                    path_map[i][j][k] = '■'
                    obstacle_list.append((k, j, i))
    print()
    print_3d(path_map)
    print(path)

 
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x, y, z = zip(*path)
    # Plot the points
    ax.scatter(x, y, z, c='b', marker='o')

    # Connect the points with lines
    ax.plot(x, y, z, c='b', linestyle='-', linewidth=2)
    if obstacle_list:
        x, y, z = zip(*obstacle_list)
        ax.scatter(x, y, z, c='r', marker='s')

    ax.set_xlim(0, len(nodes[0][0])-1)
    ax.set_ylim(0, len(nodes[0])-1)
    ax.set_zlim(0, len(nodes)-1)
    ax.set_xlabel('Length')
    ax.set_ylabel('Width')
    ax.set_zlabel('Height')
    plt.tight_layout()
    # Show the plot
    plt.show()