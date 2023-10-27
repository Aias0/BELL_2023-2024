import numpy as np, math, time, copy
nodes = [[0, 0, 0, 0, 0, 1, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 1, 0, 0, 1, 1, 0],
         [0, 0, 1, 0, 0, 0, 0],
         [1, 1, 0, 1, 0, 0, 1],
         [0, 0, 0, 0, 1, 0, 0],
         [0, 0, 0, 0, 1, 0, 0],]

def print2d(list):
    for i, r in enumerate(list):
        if i == 0:
            print(f'[{r}')
        elif i == len(list)-1:
            print(f' {r}]')
        else:
            print(f' {r}')
def index_2d(myList, v):
    for i, x in enumerate(myList):
        if v in x:
            return (i, x.index(v))

def path_find(start: tuple, end: tuple, nodes: list) -> list:
    cost_map = [[0 for i in range(len(nodes[0]))] for j in range(len(nodes))]
    surrounding_nodes = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
    def calc_cost(node: tuple):
        for change in surrounding_nodes:
            #print(node, change)
            new_node = tuple(np.add(node, change))
            if min(new_node) >= 0 and new_node[1] < len(cost_map[0]) and new_node[0] < len(cost_map):
                if nodes[new_node[1]][new_node[0]] == 1:
                    cost_map[new_node[1]][new_node[0]] = 'X'
                    return
                start_dist = math.fabs(new_node[1] - start[1]) + math.fabs(new_node[0] - start[0])
                #start_dist = ((new_node[1] - start[1])**2+(new_node[0] - start[0])**2)**0.5
                start_dist *= 0.5
                end_dist = math.fabs(end[1] - new_node[1]) + math.fabs(end[0] - new_node[0])
                #end_dist = ((end[1] - new_node[1])**2+(end[0] - new_node[0])**2)**0.5
                end_dist *= 10
                cost_map[new_node[1]][new_node[0]] = start_dist + end_dist
        #print()
    calc_cost(start)
    black_list = []
    temp = [None, None]
    while temp[1] != end:
        temp = [None, None]
        for i, row in enumerate(cost_map):
            for j, cost in enumerate(row):
                cord = (j, i)
                if cord in black_list or cost == 'X':
                    continue
                if (temp[0] == None or cost != 0) or (nodes[i][j] != 1 and cost != 0 and cost <= temp[0]):
                    temp[0] = cost
                    temp[1] = cord
        print(temp)
        black_list.append(temp[1])
        calc_cost(temp[1])
        print2d(cost_map)
        print(black_list)
    path_surrounding_nodes = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    current_node = start
    current_path = [start]
    path_black_list = []
    next_path = [None, None]
    while next_path[1] != end:
        temp = []
        for change in path_surrounding_nodes:
            new_node = tuple(np.add(current_node, change))
            if min(new_node) >= 0 and new_node[1] < len(cost_map[0]) and new_node[0] < len(cost_map):
                new_node_cost = cost_map[new_node[1]][new_node[0]]
                print(new_node_cost, new_node)
                if new_node in path_black_list or new_node_cost == 'X' or new_node_cost == 0:
                    continue
                temp.append((new_node_cost, new_node))
        print(path_black_list)
        print(temp)
        if temp:
            next_path = min(temp)
            path_black_list.append(next_path[1])
            current_path.append(next_path[1])
            current_node = next_path[1]
        else:
            print(current_path)
            path_black_list.append(current_path.pop())
            current_node = current_path[-1]

        print(current_path)
    print('Cleaning up')
    current = start
    i = 0
    prev_node = current_path[0]
    next_node = current_path[1]
    path_length = len(current_path)
    while i < path_length:
        for change in path_surrounding_nodes:
            new_node = tuple(np.add(current, change))
            if new_node in current_path and new_node != prev_node and new_node != next_node:
                print(current_path)
                print(new_node, current_path.index(new_node)+1, current, current_path.index(current))
                print(current_path[current_path.index(new_node)+1:current_path.index(current)])
                del current_path[current_path.index(current)+1:current_path.index(new_node)]
                print(current_path)
                #time.sleep(20)
                continue
        path_length = len(current_path)
        prev_node = current
        i+=1
        current = current_path[i]
        try:
            next_node = current_path[i+1]
        except:
            break
        print(i, current, next_node, path_length)
    path_map = [[' ' for i in range(len(nodes[0]))] for j in range(len(nodes))]
    for path in current_path:
        path_map[path[1]][path[0]] = 'O'
    for i, r in enumerate(nodes):
        for j, node in enumerate(r):
            if node == 1:
                path_map[i][j] = '■'
    print2d(cost_map)
    print()
    print2d(path_map)
    return current_path
    
    

path_find((0, 0), (6, 6), nodes)