# GitHub Repository: https://github.com/jkim603/enpm661-project2

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
def move_up(i, j):
    m = i
    n = j+1
    new_node = (m,n)
    cost = 1
    return new_node, cost

def move_up_right(i, j):
    m = i+1
    n = j+1
    new_node = (m,n)
    cost = 1.4
    return new_node, cost

def move_right(i, j):
    m = i+1
    n = j
    new_node = (m,n)
    cost = 1
    return new_node, cost

def move_down_right(i, j):
    m = i+1
    n = j-1
    new_node = (m,n)
    cost = 1.4
    return new_node, cost

def move_down(i, j):
    m = i
    n = j-1
    new_node = (m,n)
    cost = 1
    return new_node, cost

def move_down_left(i, j):
    m = i-1
    n = j-1
    new_node = (m,n)
    cost = 1.4
    return new_node, cost

def move_left(i, j):
    m = i-1
    n = j
    new_node = (m,n)
    cost = 1
    return new_node, cost

def move_up_left(i, j):
    m = i-1
    n = j+1
    new_node = (m,n)
    cost = 1.4
    return new_node, cost

def generate_path(node_list):
    node_states = [item[1] for item in node_list]
    state, parent = node_list[-1][1], node_list[-1][2]
    path_list = [state]
    while not parent==None:
        ind = node_states.index(parent)
        state, parent = node_list[ind][1], node_list[ind][2]
        path_list.insert(0,state)
    return path_list

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
        elif 0<=j<=4 or 595<=j<=599: #vertical wall margin
            map[i,j]=1
        elif 0<=i<=4 or 245<=i<=249: #horizonal wall margin
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
        # j = -j+599
        if i<=100 and 100<=j<=150:
            map_show[i,j]=np.array([255,0,155]) #bottom rectangle obstacle
        elif 100<i<=105 and 100<=j<=150:
            map_show[i,j]=np.array([100,0,255]) #bottom rectangle margin
        elif i<=105 and (95<=j<100 or 150<j<=155):
            map_show[i,j]=np.array([100,0,255]) #bottom rectangle margin
        elif i>=150 and 100<=j<=150:
            map_show[i,j]=np.array([255,0,155]) #top rectangle obstacle
        elif 150>i>=145 and 100<=j<=150:
            map_show[i,j]=np.array([100,0,255]) #top rectangle margin
        elif i>=145 and (95<=j<100 or 150<j<=155):
            map_show[i,j]=np.array([100,0,255]) #top rectangle margin
        elif j>=460 and i>=2*j-895 and i<=-2*j+1145: 
            map_show[i,j]=np.array([255,0,155]) #triangle obstacle
        elif 460>j>=455 and 2*j-895<=i<=-2*j+1145 and 20<=i<=230:
            map_show[i,j]=np.array([100,0,255]) #triangle margin
        elif 510>=j>=455 and ((2*j-895>i>=2*j-906 and i>=20) or (-2*j+1145<i<=-2*j+1156 and i<=230)):
            map_show[i,j]=np.array([100,0,255]) #triangle margin
        elif 515>=j>510 and 2*j-906<=i<=-2*j+1156:
            map_show[i,j]=np.array([100,0,255]) #triangle margin
        elif 235<=j<=365 and i<=0.5774*j+26.7949 and i<=-0.5774*j+373.2051 and i>=-0.5774*j+223.2051 and i>=0.5774*j-123.2051:
            map_show[i,j]=np.array([255,0,155]) #hexagon obstacle
        elif 230<=j<235 and 0.5774*j-48.2051<=i<=-0.5774*j+298.2051:
            map_show[i,j]=np.array([100,0,255]) #hexagon margin
        elif 365<j<=370 and 0.5774*j-48.2051>=i>=-0.5774*j+298.2051:
            map_show[i,j]=np.array([100,0,255]) #hexagon margin
        elif 230<=j<=300 and (0.5774*j+26.7949<i<=0.5774*j+32.7949 or -0.5774*j+223.2051>i>=-0.5774*j+217.2051):
            map_show[i,j]=np.array([100,0,255]) #hexagon margin
        elif 300<=j<=370 and (-0.5774*j+373.2051<i<=-0.5774*j+379.2051 or 0.5774*j-123.2051>i>=0.5774*j-129.2051):
            map_show[i,j]=np.array([100,0,255]) #hexagon margin
        elif 0<=j<=4 or 595<=j<=599: 
            map_show[i,j]=np.array([100,0,255]) #vertical wall margin
        elif 0<=i<=4 or 245<=i<=249: 
            map_show[i,j]=np.array([100,0,255]) #horizonal wall margin

# request inputs and check that they are within map bounds and not in an obstacle
while 1:
    try:
        start_input = input("Start State: x,y:")
        node_state_i = input2node(start_input)
        # if node_state_i[0]<0 or node_state_i[0]>599 or node_state_i[1]<0 or node_state_i[1]>249:
        #     print('Start State outside of acceptable input range. X input range: 1 to 600. Y input range: 1 to 250. Try again...')
        if map[node_state_i[1],node_state_i[0]]==1:
            print('Start State inside an obstacle. Try again...')
        else:
            break
    except:
        print('Input must be two integers separated by a comma (ex: 10,10). Acceptable range for first value: 1 to 600. Acceptable range for second value: 1 to 250. Try again...')

while 1:
    try:
        goal_input = input("Goal State: x,y:")
        goal_state = input2node(goal_input)
        # if goal_state[0]<0 or goal_state[0]>599 or goal_state[1]<0 or goal_state[1]>249:
        #     print('Goal State outside of acceptable input range. X input range: 1 to 600. Y input range: 1 to 250. Try again...')
        if map[goal_state[1],goal_state[0]]==1:
            print('Goal State inside an obstacle. Try again...')
        else:
            print('Inputs accepted! Calculating...')
            break
    except:
        print('Input must be two integers separated by a comma (ex: 10,10). Acceptable range for first value: 1 to 600. Acceptable range for second value: 1 to 250. Try again...')

node_parent_i = None
node_cost_i = 0
node_info_i = [node_cost_i, node_state_i, node_parent_i]

nodes_open = [node_info_i]
nodes_closed = []

nodes_open.sort(key = lambda x: x[0])
current_node = nodes_open.pop(0)
current_cost, current_state = current_node[0], current_node[1]

# pop a node, generate child nodes, compare and update lists
while not current_state==goal_state:
    # print(current_state)
    node_parent_i, x_coord, y_coord = current_state, current_state[0], current_state[1]
    nodes_closed.append(current_node)

    while map[y_coord+1, x_coord]==0:
        node_state_i, cost_i = move_up(x_coord, y_coord) #generate new node, if not in obstacle space
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
    
    while map[y_coord+1, x_coord+1]==0:
        node_state_i, cost_i = move_up_right(x_coord, y_coord) #generate new node, if not in obstacle space
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
    
    while map[y_coord, x_coord+1]==0:
        node_state_i, cost_i = move_right(x_coord, y_coord) #generate new node, if not in obstacle space
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
    
    while map[y_coord-1, x_coord+1]==0:
        node_state_i, cost_i = move_down_right(x_coord, y_coord) #generate new node, if not in obstacle space
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

    while map[y_coord-1, x_coord]==0:
        node_state_i, cost_i = move_down(x_coord, y_coord) #generate new node, if not in obstacle space
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

    while map[y_coord-1, x_coord-1]==0:
        node_state_i, cost_i = move_down_left(x_coord, y_coord) #generate new node, if not in obstacle space
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

    while map[y_coord, x_coord-1]==0:
        node_state_i, cost_i = move_left(x_coord, y_coord) #generate new node, if not in obstacle space
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

    while map[y_coord+1, x_coord-1]==0:
        node_state_i, cost_i = move_up_left(x_coord, y_coord) #generate new node, if not in obstacle space
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

    nodes_open.sort(key = lambda x: x[0])
    current_node = nodes_open.pop(0)
    current_cost, current_state = current_node[0], current_node[1]

nodes_closed.append(current_node)
print("Complete! Confirm final state:",'('+str(current_state[0]+1)+', '+str(current_state[1]+1)+')')

path = generate_path(nodes_closed)
# print(path)

# print('check 1')
# visualize map grid search and final path
img_array = [map_show]
# print('check 1a')
# print(len(nodes_closed))
# for node in nodes_closed:
for n in range(len(nodes_closed)):
    # print('check 1b')
    # x_coord, y_coord = node[1][0], 249-node[1][1]
    x_coord, y_coord = nodes_closed[n][1][0], 249-nodes_closed[n][1][1]
    # print('check 1c')
    map_show[y_coord, x_coord] = np.array([220,255,0]) #update color of pixels as they are explored
    # print('check 1d')
    img_array.append(map_show.copy())
    # print('check 1e')
# print('check 2')
# for state in path:
for s in range(len(path)):
    x_coord, y_coord = path[s][0], 249-path[s][1]
    map_show[y_coord, x_coord] = np.array([200,0,0]) #update color of optimal path as it is traveled
    img_array.append(map_show.copy())

# print('check 3')
# write to video file
size = (600,250)
vid = cv.VideoWriter('proj2_video_julia_kim.mp4', cv.VideoWriter_fourcc(*'mp4v'), 1000, size)
# print('check 4')
for k in range(len(img_array)):
    img = img_array[k]
    vid.write(img)
# print('check 5')
vid.release()
cv.destroyAllWindows()

print('check 6')
end_time = time.time()
print('Total time (s):', end_time-start_time)