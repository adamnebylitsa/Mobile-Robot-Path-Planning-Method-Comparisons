from graph import Graph
import numpy as np
from numpy import random

def plan_path(start_point,end_point,robot_radius,environment_grid, iteration_number = 500):
    # initialize graph
    graph=Graph()
    graph[start_point]=[]
    graph["parents"] = {start_point:None}

    path_found = False
    path = None

    grid_shape=environment_grid.shape
    valuesX=np.linspace(0,grid_shape[0]/4,grid_shape[0]+1)
    valuesY=np.linspace(0,grid_shape[1]/4,grid_shape[1]+1)


    while len(graph)<iteration_number:
        new_position = (random.choice(valuesX),random.choice(valuesY))
        if Graph.in_obstacle(environment_grid,new_position,robot_radius):
            continue
        nearest=graph.nearest_point(new_position)
        #You can clean/change some of these methods if needed
        if Graph.clear_path(environment_grid,new_position,nearest,robot_radius):
            graph[nearest].append(new_position)
            if new_position not in graph:
                graph[new_position]=[]
                graph['parents'][new_position] = nearest
            graph[new_position].append(nearest)

            # check if clear path from most recent point to end point
            if Graph.clear_path(environment_grid, end_point, new_position, robot_radius):
                graph[new_position].append(end_point)
                if end_point not in graph:
                    graph[end_point] = []
                    graph["parents"][end_point] = new_position
                graph[end_point].append(new_position)
                path_found = True
                break
            
    if path_found:
        path = graph.get_path(start_point, end_point)
    
    return graph, path

if __name__=="__main__":
    env = Graph.createEnvironment("environments/environment3.txt")
    grid, ax=Graph.occupancyGrid(env, show=False)
    start=(1,1)
    end=(28,28)
    radius=.5
    graph, path =plan_path(start,end,radius,grid, 500)
    print(path)
    graph.showGraph(path, ax)
    # print(graph)
