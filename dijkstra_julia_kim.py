import numpy as np
import cv2 as cv

# define function to convert user input into tuple
def input2tup(input):
    in_list = []
    for num in input.split(','):
        in_list.append(int(num)-1)
    output = tuple(in_list)
    return output

# define actions as 8 separate functions
def move_up(node_status, map):
    i = node_status[0]
    j = 249-node_status[1]
    if map[j+1, i] == 0:
        m = i
        n = j+1
        new_node = (m,n)
        cost = 1
    return new_node, cost

def move_up_right(node_status, map):
    i = node_status[0]
    j = 249-node_status[1]
    if map[j+1, i+1] == 0:
        m = i+1
        n = j+1
        new_node = (m,n)
        cost = 1.4
    return new_node, cost

def move_right(node_status, map):
    i = node_status[0]
    j = 249-node_status[1]
    if map[j, i+1] == 0:
        m = i+1
        n = j
        new_node = (m,n)
        cost = 1
    return new_node, cost

def move_down_right(node_status, map):
    i = node_status[0]
    j = 249-node_status[1]
    if map[j-1, i+1] == 0:
        m = i+1
        n = j-1
        new_node = (m,n)
        cost = 1.4
    return new_node, cost

def move_down(node_status, map):
    i = node_status[0]
    j = 249-node_status[1]
    if map[j-1, i] == 0:
        m = i
        n = j-1
        new_node = (m,n)
        cost = 1
    return new_node, cost

def move_down_left(node_status, map):
    i = node_status[0]
    j = 249-node_status[1]
    if map[j-1, i-1] == 0:
        m = i-1
        n = j-1
        new_node = (m,n)
        cost = 1.4
    return new_node, cost

def move_left(node_status, map):
    i = node_status[0]
    j = 249-node_status[1]
    if map[j, i-1] == 0:
        m = i-1
        n = j
        new_node = (m,n)
        cost = 1
    return new_node, cost

def move_up_left(node_status, map):
    i = node_status[0]
    j = 249-node_status[1]
    if map[j+1, i-1] == 0:
        m = i-1
        n = j+1
        new_node = (m,n)
        cost = 1.4
    return new_node, cost

start_input = input("Start State:")
goal_input = input("Goal State:")
# node_state_i = start_input
# goal_state = goal_input

node_state_i = input2tup(start_input)
goal_state = input2tup(goal_input)
# print(node_state_i)
# print(type(node_state_i))

# print(node_state_i)
# print(goal_state)
node_index_i = 0
node_parent_index_i = None
node_info_i = (node_state_i, node_index_i, node_parent_index_i)

# nodes_all = [node_info_i]
nodes_test = [node_info_i]
states_visited = []

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


# cv.imshow('Binary Map',map)
# cv.imshow('Colorful Map',map_show)
# cv.waitKey(0)
# cv.destroyAllWindows()