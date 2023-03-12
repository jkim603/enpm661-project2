import numpy as np
import cv2 as cv
import time

start_time = time.time()

# define function to convert user input into tuple and format used for nodes
def input2node(input):
    in_list = []
    for num in input.split(','):
        in_list.append(int(num)-1)
    output = tuple(in_list)
    return output

# define actions as 8 separate functions
def move_up(node_status, i, j, map):
    if map[j+1, i] == 0:
        m = i
        n = j+1
        new_node = (m,n)
        cost = 1
        return new_node, cost
    else:
        return node_status, 0

def move_up_right(node_status, i, j, map):
    if map[j+1, i+1] == 0:
        m = i+1
        n = j+1
        new_node = (m,n)
        cost = 1.4
        return new_node, cost
    else:
        return node_status, 0

def move_right(node_status, i, j, map):
    if map[j, i+1] == 0:
        m = i+1
        n = j
        new_node = (m,n)
        cost = 1
        return new_node, cost
    else:
        return node_status, 0

def move_down_right(node_status, i, j, map):
    if map[j-1, i+1] == 0:
        m = i+1
        n = j-1
        new_node = (m,n)
        cost = 1.4
        return new_node, cost
    else:
        return node_status, 0

def move_down(node_status, i, j, map):
    if map[j-1, i] == 0:
        m = i
        n = j-1
        new_node = (m,n)
        cost = 1
        return new_node, cost
    else:
        return node_status, 0

def move_down_left(node_status, i, j, map):
    if map[j-1, i-1] == 0:
        m = i-1
        n = j-1
        new_node = (m,n)
        cost = 1.4
        return new_node, cost
    else:
        return node_status, 0

def move_left(node_status, i, j, map):
    if map[j, i-1] == 0:
        m = i-1
        n = j
        new_node = (m,n)
        cost = 1
        return new_node, cost
    else:
        return node_status, 0

def move_up_left(node_status, i, j, map):
    if map[j+1, i-1] == 0:
        m = i-1
        n = j+1
        new_node = (m,n)
        cost = 1.4
        return new_node, cost
    else:
        return node_status, 0

# define a function to compare if two nodes are the same, used to check if goal reached
# def node_compare(node1, node2):
#     i1 = node1[0]
#     j1 = node1[1]
#     i2 = node2[0]
#     j2 = node2[1]
#     if i1==i2 and j1==j2:
#         return True
#     else:
#         return False

# define a function to determine if a node is already in a list
# def node_in_list(node_state, node_list):
#     state_list = []
#     for node in node_list:
#         state_list.append(node[1])
#     if node_state in state_list:
#         return True
#     else:
#         return False

# define a function to sort the list by lowest cost to come
def sort_cost(node_list):
    node_list.sort(key = lambda x: x[0])
    return node_list

# define map space with 5mm clearance; 0=free space, 1=obstacle space
map = np.zeros((250,600))
for i in range(250):
    # print('i',i)
    i = -i+249
    for j in range(600):
        # print('j',j)
        j = -j+599
        if i<=105 and 95<=j<=155: #bottom rectangle definition w/ margin
            map[i,j]=1
        elif i>=145 and 95<=j<=155: #top rectangle definition w/ margin
            map[i,j]=1
        elif j>=455 and i>=2*j-906 and i<=-2*j+1156 and 20<=i<=230: #triangle definition w/ margin
            map[i,j]=1
        elif 230<=j<=370 and i<=0.5774*j+32.7949 and i<=-0.5774*j+379.2051 and i>=-0.5774*j+217.2051 and i>=0.5774*j-129.2051: #hexagon definiton w/ margin
            map[i,j]=1

# define a prettier version of map space for visualizations
map_show = np.zeros((250,600,3), np.uint8)
map_show[:,:] = np.array([255,255,255])
# map_show = cv.cvtColor(map, cv.COLOR_GRAY2BGR)
for i in range(250):
    # print('i',i)
    i = -i+249
    for j in range(600):
        # print('j',j)
        j = -j+599
        if i<=100 and 100<=j<=150:
            map_show[i,j]=np.array([255,0,125]) #bottom rectangle obstacle
        elif 100<i<=105 and 100<=j<=150:
            map_show[i,j]=np.array([255,0,200]) #bottom rectangle margin
        elif i<=105 and (95<=j<100 or 150<j<=155):
            map_show[i,j]=np.array([255,0,200]) #bottom rectangle margin
        elif i>=150 and 100<=j<=150:
            map_show[i,j]=np.array([255,0,125]) #top rectangle obstacle
        elif 150>i>=145 and 100<=j<=150:
            map_show[i,j]=np.array([255,0,200]) #top rectangle margin
        elif i>=145 and (95<=j<100 or 150<j<=155):
            map_show[i,j]=np.array([255,0,200]) #top rectangle margin
        elif j>=460 and i>=2*j-895 and i<=-2*j+1145: 
            map_show[i,j]=np.array([255,0,125]) #triangle obstacle
        elif 460>j>=455 and 2*j-895<=i<=-2*j+1145 and 20<=i<=230:
            map_show[i,j]=np.array([255,0,200]) #triangle margin
        elif 510>=j>=455 and ((2*j-895>i>=2*j-906 and i>=20) or (-2*j+1145<i<=-2*j+1156 and i<=230)):
            map_show[i,j]=np.array([255,0,200]) #triangle margin
        elif 515>=j>510 and 2*j-906<=i<=-2*j+1156:
            map_show[i,j]=np.array([255,0,200]) #triangle margin
        elif 235<=j<=365 and i<=0.5774*j+26.7949 and i<=-0.5774*j+373.2051 and i>=-0.5774*j+223.2051 and i>=0.5774*j-123.2051:
            map_show[i,j]=np.array([255,0,125]) #hexagon obstacle
        elif 230<=j<235 and 0.5774*j-48.2051<=i<=-0.5774*j+298.2051:
            map_show[i,j]=np.array([255,0,200]) #hexagon margin
        elif 365<j<=370 and 0.5774*j-48.2051>=i>=-0.5774*j+298.2051:
            map_show[i,j]=np.array([255,0,200]) #hexagon margin
        elif 230<=j<=300 and (0.5774*j+26.7949<i<=0.5774*j+32.7949 or -0.5774*j+223.2051>i>=-0.5774*j+217.2051):
            map_show[i,j]=np.array([255,0,200]) #hexagon margin
        elif 300<=j<=370 and (-0.5774*j+373.2051<i<=-0.5774*j+379.2051 or 0.5774*j-123.2051>i>=0.5774*j-129.2051):
            map_show[i,j]=np.array([255,0,200]) #hexagon margin

start_input = input("Start State:")
goal_input = input("Goal State:")
# node_state_i = start_input
# goal_state = goal_input

node_state_i = input2node(start_input)
goal_state = input2node(goal_input)
# print(node_state_i)
# print(type(node_state_i))

# print(node_state_i)
# print(goal_state)
# node_index_i = 0
node_parent_i = None
node_cost_i = 0
node_info_i = [node_cost_i, node_state_i, node_parent_i]

# nodes_all = [node_info_i]
nodes_open = [node_info_i]
nodes_closed = []

nodes_open = sort_cost(nodes_open)
current_node = nodes_open.pop(0)
current_cost = current_node[0]
current_state = current_node[1]
# print(current_state)

# pop a node, generate child nodes, compare and update lists
while not current_state==goal_state:
    print(current_state)
    node_parent_i, x_coord, y_coord = current_state, current_state[0], current_state[1]
    nodes_closed.append(current_node)

    while y_coord+1<=249:
        node_state_i, cost_i = move_up(current_state, x_coord, y_coord, map) #generate new node, if not in obstacle space (defined in function)
        node_cost_i = current_cost + cost_i
        closed_check = [item[1] for item in nodes_closed]
        if node_state_i in closed_check: #check if new node in closed list
            break
        else:
            open_check = [item[1] for item in nodes_open]
            if node_state_i in open_check: #check if new node in open list
                idx=open_check.index(node_state_i)
                if node_cost_i<nodes_open[idx][0]: #compare cost between multiple paths to reach node, update open list if new cost is lower
                    nodes_open[idx][0] = node_cost_i
                    nodes_open[idx][2] = node_parent_i
                break
            else:
                node_info_i = [node_cost_i, node_state_i, node_parent_i] #if new node not in open list already, add to open list
                nodes_open.append(node_info_i)
                break
    
    while y_coord+1<=249 and x_coord+1<=599:
        node_state_i, cost_i = move_up_right(current_state, x_coord, y_coord, map) #generate new node, if not in obstacle space (defined in function)
        node_cost_i = current_cost + cost_i
        closed_check = [item[1] for item in nodes_closed]
        if node_state_i in closed_check: #check if new node in closed list
            break
        else:
            open_check = [item[1] for item in nodes_open]
            if node_state_i in open_check: #check if new node in open list
                idx=open_check.index(node_state_i)
                if node_cost_i<nodes_open[idx][0]: #compare cost between multiple paths to reach node, update open list if new cost is lower
                    nodes_open[idx][0] = node_cost_i
                    nodes_open[idx][2] = node_parent_i
                break
            else:
                node_info_i = [node_cost_i, node_state_i, node_parent_i] #if new node not in open list already, add to open list
                nodes_open.append(node_info_i)
                break
    
    while x_coord+1<=599:
        node_state_i, cost_i = move_right(current_state, x_coord, y_coord, map) #generate new node, if not in obstacle space (defined in function)
        node_cost_i = current_cost + cost_i
        closed_check = [item[1] for item in nodes_closed]
        if node_state_i in closed_check: #check if new node in closed list
            break
        else:
            open_check = [item[1] for item in nodes_open]
            if node_state_i in open_check: #check if new node in open list
                idx=open_check.index(node_state_i)
                if node_cost_i<nodes_open[idx][0]: #compare cost between multiple paths to reach node, update open list if new cost is lower
                    nodes_open[idx][0] = node_cost_i
                    nodes_open[idx][2] = node_parent_i
                break
            else:
                node_info_i = [node_cost_i, node_state_i, node_parent_i] #if new node not in open list already, add to open list
                nodes_open.append(node_info_i)
                break
    
    while y_coord-1>=0 and x_coord+1<=599:
        node_state_i, cost_i = move_down_right(current_state, x_coord, y_coord, map) #generate new node, if not in obstacle space (defined in function)
        node_cost_i = current_cost + cost_i
        closed_check = [item[1] for item in nodes_closed]
        if node_state_i in closed_check: #check if new node in closed list
            break
        else:
            open_check = [item[1] for item in nodes_open]
            if node_state_i in open_check: #check if new node in open list
                idx=open_check.index(node_state_i)
                if node_cost_i<nodes_open[idx][0]: #compare cost between multiple paths to reach node, update open list if new cost is lower
                    nodes_open[idx][0] = node_cost_i
                    nodes_open[idx][2] = node_parent_i
                break
            else:
                node_info_i = [node_cost_i, node_state_i, node_parent_i] #if new node not in open list already, add to open list
                nodes_open.append(node_info_i)
                break

    while y_coord-1>=0:
        node_state_i, cost_i = move_down(current_state, x_coord, y_coord, map) #generate new node, if not in obstacle space (defined in function)
        node_cost_i = current_cost + cost_i
        closed_check = [item[1] for item in nodes_closed]
        if node_state_i in closed_check: #check if new node in closed list
            break
        else:
            open_check = [item[1] for item in nodes_open]
            if node_state_i in open_check: #check if new node in open list
                idx=open_check.index(node_state_i)
                if node_cost_i<nodes_open[idx][0]: #compare cost between multiple paths to reach node, update open list if new cost is lower
                    nodes_open[idx][0] = node_cost_i
                    nodes_open[idx][2] = node_parent_i
                break
            else:
                node_info_i = [node_cost_i, node_state_i, node_parent_i] #if new node not in open list already, add to open list
                nodes_open.append(node_info_i)
                break

    while y_coord-1>=0 and x_coord-1>=0:
        node_state_i, cost_i = move_down_left(current_state, x_coord, y_coord, map) #generate new node, if not in obstacle space (defined in function)
        node_cost_i = current_cost + cost_i
        closed_check = [item[1] for item in nodes_closed]
        if node_state_i in closed_check: #check if new node in closed list
            break
        else:
            open_check = [item[1] for item in nodes_open]
            if node_state_i in open_check: #check if new node in open list
                idx=open_check.index(node_state_i)
                if node_cost_i<nodes_open[idx][0]: #compare cost between multiple paths to reach node, update open list if new cost is lower
                    nodes_open[idx][0] = node_cost_i
                    nodes_open[idx][2] = node_parent_i
                break
            else:
                node_info_i = [node_cost_i, node_state_i, node_parent_i] #if new node not in open list already, add to open list
                nodes_open.append(node_info_i)
                break

    while x_coord-1>=0:
        node_state_i, cost_i = move_left(current_state, x_coord, y_coord, map) #generate new node, if not in obstacle space (defined in function)
        node_cost_i = current_cost + cost_i
        closed_check = [item[1] for item in nodes_closed]
        if node_state_i in closed_check: #check if new node in closed list
            break
        else:
            open_check = [item[1] for item in nodes_open]
            if node_state_i in open_check: #check if new node in open list
                idx=open_check.index(node_state_i)
                if node_cost_i<nodes_open[idx][0]: #compare cost between multiple paths to reach node, update open list if new cost is lower
                    nodes_open[idx][0] = node_cost_i
                    nodes_open[idx][2] = node_parent_i
                break
            else:
                node_info_i = [node_cost_i, node_state_i, node_parent_i] #if new node not in open list already, add to open list
                nodes_open.append(node_info_i)
                break

    while y_coord+1<=249 and x_coord-1>=0:
        node_state_i, cost_i = move_up_left(current_state, x_coord, y_coord, map) #generate new node, if not in obstacle space (defined in function)
        node_cost_i = current_cost + cost_i
        closed_check = [item[1] for item in nodes_closed]
        if node_state_i in closed_check: #check if new node in closed list
            break
        else:
            open_check = [item[1] for item in nodes_open]
            if node_state_i in open_check: #check if new node in open list
                idx=open_check.index(node_state_i)
                if node_cost_i<nodes_open[idx][0]: #compare cost between multiple paths to reach node, update open list if new cost is lower
                    nodes_open[idx][0] = node_cost_i
                    nodes_open[idx][2] = node_parent_i
                break
            else:
                node_info_i = [node_cost_i, node_state_i, node_parent_i] #if new node not in open list already, add to open list
                nodes_open.append(node_info_i)
                break

    nodes_open = sort_cost(nodes_open)
    current_node, current_cost, current_state = nodes_open.pop(0), current_node[0], current_node[1]



end_time = time.time()
print('Total time (s):', end_time-start_time)

# cv.imshow('Binary Map',map)
# cv.imshow('Colorful Map',map_show)
# cv.waitKey(0)
# cv.destroyAllWindows()