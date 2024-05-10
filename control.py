from graph import Graph
import numpy as np
from numpy import random
import matplotlib.pyplot as plt

def plan_path(start_point,end_point,robot_radius,environment_grid, iteration_number = 500):
    # initialize graph
    graph=Graph(start_point=start_point)
    
    path_found = False
    path = None

    grid_shape=environment_grid.shape
    valuesX=np.linspace(robot_radius,(grid_shape[0] -robot_radius)/4,grid_shape[0]+1)
    valuesY=np.linspace(robot_radius,(grid_shape[1]-robot_radius)/4,grid_shape[1]+1)

    while len(graph)<iteration_number:
        new_position = (random.choice(valuesX),random.choice(valuesY))
        if new_position in graph or Graph.in_obstacle(environment_grid,new_position,robot_radius):
            continue
        nearest=graph.nearest_point(new_position)
        #You can clean/change some of these methods if needed
        if Graph.clear_path(environment_grid,new_position,nearest,robot_radius):
            graph[nearest][1].append(new_position)
            if new_position not in graph:
                graph[new_position]=[0,[]]
                graph['parents'][new_position] = nearest
            graph[new_position][1].append(nearest)

            # check if clear path from most recent point to end point
            if Graph.clear_path(environment_grid, end_point, new_position, robot_radius):
                graph[new_position][1].append(end_point)
                if end_point not in graph:
                    graph[end_point] = [0,[]]
                    graph["parents"][end_point] = new_position
                graph[end_point][1].append(new_position)
                path_found = True
                break
            
    if path_found:
        path = graph.get_path(start_point, end_point)
    
    return graph, path

if __name__=="__main__":
    env = Graph.createEnvironment("environments/environment2.txt")
    grid, ax=Graph.occupancyGrid(env, show=False)
    start=(1,1)
    end=(28,28)
    radius=.5
    graph, path =plan_path(start,end,radius,grid, 500)
    # print(path)
    print (Graph.getPathLength(path))
    graph.showGraph(path, ax, show=True)
    # print(graph)
