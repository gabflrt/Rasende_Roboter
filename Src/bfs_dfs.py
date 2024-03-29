from grid import *
import numpy as np
from collections import deque #Usefull for FIFO in BFS

class Node:

    def __init__(self,_state:dict,_father_node):

        #state -> Will be representing by a list of the position of the robot
        #father_node-> Will be the father node
        self.state = _state
        self.father_node = _father_node

def BFS_or_DFS(empty_grid:Grid, initial_node_state:Node,color_mission:Color,coordinate_mission:tuple,is_BFS:bool):
    if is_BFS:
        fifo_state = deque()
        visited_state = deque()
    
        fifo_state.append(initial_node_state)
        temp_coordinate = initial_node_state.state[color_mission]
        start_time = time.time()

        while (len(fifo_state) != 0 and temp_coordinate != coordinate_mission):

            print("Processing...")
            process_node = fifo_state.popleft()
            visited_state.append(process_node.state)
            temp_coordinate = process_node.state[color_mission]

            is_find,node_find = next_state(process_node,empty_grid,fifo_state,visited_state,color_mission,coordinate_mission)
            if is_find:
                print("We have found a path")
                print("Final node: ",process_node.state)
                print("Mission color: ",color_mission)
                print("Mission color: ", coordinate_mission)
                path = find_final_path(node_find)
                end_time = time.time() 
                elapsed_time = end_time - start_time
                print(f"Time elapsed: {elapsed_time} seconds")
                print(f"Number of state that have been visited:{len(visited_state)}")
                print(f"State/s: {len(visited_state) / elapsed_time:.0f}")
                return path


        if len(fifo_state) != 0:
            return None
    else:
        
        stack_state = [initial_node_state]
        visited_state = deque()
        temp_coordinate = initial_node_state.state[color_mission]
        start_time = time.time()

        while stack_state and temp_coordinate != coordinate_mission:
            process_node = stack_state.pop()
            if process_node.state not in visited_state:
                visited_state.append(process_node.state)
            temp_coordinate = process_node.state[color_mission]
            print('processing....')

            is_find, node_find = next_state(process_node, empty_grid, stack_state, visited_state, color_mission, coordinate_mission)

            if is_find:
                print("We have found a path")
                print("Final node: ", process_node.state)
                print("Mission color: ", color_mission)
                print("Mission coordinate: ", coordinate_mission)
                path = find_final_path(node_find)
                end_time = time.time()
                elapsed_time = end_time - start_time
                print(f"Time elapsed: {elapsed_time} seconds")
                print(f"Number of states that have been visited: {len(visited_state)}")
                print(f"States/s: {len(visited_state) / elapsed_time:.0f}")
                
                return path

        if not stack_state:
            return None


 

def add_status_empty_grid(grid:Grid,status:dict):
    for color in status:
        grid.add_status(color,status[color][0],status[color][1])
    grid.actualize_robot_position()
        


def clean_all_status(grid:Grid,status:dict):
    for color in status:
        grid.clean_status(status[color][0],status[color][1])    
    grid.actualize_robot_position()    



def is_already_visited(status,visited_state:deque,color_:Color):
    
    for state in visited_state:
        if state[color_] == status[color_]:
            return True
    return False
    


def next_state(node_state:Node,empty_grid:Grid,fifo_state:deque,visited_state:deque,color_mission:Color,coordinate_mission:tuple):

    test_goal = False    
    add_status_empty_grid(empty_grid,node_state.state)
    empty_grid.possible_move()
    for color,moves in empty_grid.possible_move_per_robot.items():
        # print(color)
        for move in moves:
            # print(list(move.values())[0])
            coordinates = list(move.values())[0]
            status_temp = dict(node_state.state) 
            status_temp[color] = coordinates
            if not is_already_visited(status_temp,visited_state,color):
                temp_node = Node(status_temp, node_state)
                fifo_state.append(temp_node)
                if status_temp[color_mission] == coordinate_mission:
                    test_goal = True
                    return test_goal, temp_node

    clean_all_status(empty_grid,node_state.state)
    return test_goal,None



def find_final_path(final_node:Node):

    list_state = []
    list_state.append(final_node.state)
    father_node = final_node.father_node
    while father_node != None:
        list_state.append(father_node.state)
        father_node = father_node.father_node    
    real_state = list_state[::-1]
    return real_state, len(real_state)-1


