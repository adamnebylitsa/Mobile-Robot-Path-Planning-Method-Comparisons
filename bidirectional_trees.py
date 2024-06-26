# Using method described here (Section 3): https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=844730
# Basically make two graphs, extend one, try to connect from the other, and switch until connected

from graph import Graph
import numpy as np
from numpy import random
import matplotlib.pyplot as plt
import time

def plan_path(start_point,end_point,robot_radius,environment_grid, iteration_number = 500):
    # initialize graphs
    start_graph=Graph(start_point=start_point)
    end_graph = Graph(start_point=end_point)
    
    path_found = False
    merge_point = None
    path = None
    
    count = 0
    grid_shape=environment_grid.shape
    valuesX=np.linspace(robot_radius,(grid_shape[0] -robot_radius)/4,grid_shape[0]+1)
    valuesY=np.linspace(robot_radius,(grid_shape[1]-robot_radius)/4,grid_shape[1]+1)

    current_graph = start_graph
    while len(start_graph)<iteration_number or len(end_graph)<iteration_number:
        count+=1
        
        new_position = (random.choice(valuesX),random.choice(valuesY))
        # if count%100 == 0:
            # print(f"iteration count: {count}")

        if Graph.in_obstacle(environment_grid,new_position,robot_radius):
            continue
        nearest=current_graph.nearest_point(new_position)
        # Extending one graph
        if Graph.clear_path(environment_grid,new_position,nearest,robot_radius):
            current_graph[nearest][1].append(new_position)
            if new_position not in current_graph:
                current_graph[new_position]=[0,[]]
                current_graph['parents'][new_position] = nearest
            current_graph[new_position][1].append(nearest)

            # Attempt to connect the other graph to the previously extended graph
            alternate_graph = end_graph if current_graph is start_graph else start_graph
            alternate_nearest = alternate_graph.nearest_point(new_position)
            if Graph.clear_path(environment_grid, new_position, alternate_nearest, robot_radius):
                alternate_graph[alternate_nearest][1].append(new_position)
                if new_position not in alternate_graph:
                    alternate_graph[new_position] = [0,[]]
                    alternate_graph["parents"][new_position] = alternate_nearest
                alternate_graph[new_position][1].append(alternate_nearest)
                merge_point = new_position
                path_found = True
                break
                
            # swap graphs
            current_graph = start_graph if current_graph is not start_graph else end_graph
            
    # if path_found:
    #     path = Graph.joinGraphs(start_graph, end_graph, start_point, end_point, merge_point)

    return start_graph, end_graph, path_found, merge_point

if __name__=="__main__":
    env_file = "environments/environment3.txt"
    env_name = env_file.split('/')[1].split('.')[0].upper().split(".")[0]
    env_num = env_name[-1]
    start_end_dict = {"1": [(1,1), (28,28)],    
                      "2": [(1,1), (20,28)],
                      "3": [(1,1), (19,28)],
                      "4": [(1,1), (28,28)],
                      "5": [(1,1), (20,15)]}
    
    env = Graph.createEnvironment(env_file)
    grid, ax=Graph.occupancyGrid(env, show=False)
    start= start_end_dict[env_num][0]
    end= start_end_dict[env_num][1]
    radius=.5
    ax.set_title(env_name.upper()[:-1] + " " + env_num)

    num_iterations = 2000
    start_time = time.perf_counter()
    start_graph, end_graph, path_found, merge_point =plan_path(start,end,radius,grid, num_iterations)
    path_time = time.perf_counter()

    path = Graph.joinGraphs(start_graph, end_graph, start, end, merge_point)
    find_path_time = time.perf_counter()


    if not path_found:
        print(f'No path found after {num_iterations} iterations')
    else:
        distance = (Graph.getPathLength(path))
        

    t1 = path_time - start_time
    t2 = find_path_time - path_time
    total_runtime = t2+t1
    num_nodes = len(start_graph) + len(end_graph)
    path_nodes = len(path)
    
    # print(f"Time to get from start point to end point: {t1}")
    # print(f"Time to find path: {t2}")
    print(f"Total runtime: {total_runtime}")
    print(f"Total distance: {distance}")
    print(f"Number of nodes in path: {path_nodes}")
    print(f"Number of nodes in graph: {num_nodes}")
    ax.set_title(env_name.upper()[:-1] + " " + env_num + " Bi-directional Method")
    start_graph.showGraph(ax =ax, show=False, node_color = 'go')
    end_graph.showGraph(path, ax, show=True, node_color= 'bo')
