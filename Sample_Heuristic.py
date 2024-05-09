from graph import Graph
import numpy as np
from numpy import random

# might switch which technique this is for based on what we think for the third case

def plan_path(start_point,end_point,robot_radius,environment_grid, iteration_number = 500,attempts=10):
    # initialize graph
    graph=Graph()
    graph[start_point]=[0,[]]
    graph["parents"] = {start_point:None}

    path_found = False
    path = None
    already_tried=[]

    grid_shape=environment_grid.shape
    valuesX=np.linspace(0,grid_shape[0]/4,grid_shape[0]+1)
    valuesY=np.linspace(0,grid_shape[1]/4,grid_shape[1]+1)


    while len(graph)<iteration_number:
        #find nearest point to the end position
        near_end=graph.nearest_point(end_point,ignore=already_tried)
        # if all of the graph is already attempted the limit number just choice a pure random point
        if near_end==None:
            new_position = (random.choice(valuesX),random.choice(valuesY))
        else:
            graph[near_end][0]+=1
            #print(near_end,graph[near_end][0])
            if graph[near_end][0]>attempts:
                already_tried.append(near_end)
            x_start=0
            y_start=0
            x_end=len(valuesX)
            y_end=len(valuesY)
            if end_point[0]>near_end[0]:
                x_start=int(near_end[0]*4)
            else:
                x_end=int(near_end[0]*4)
            if end_point[1]>near_end[1]:
                y_start=int(near_end[1]*4)
            else:
                y_end=int(near_end[1]*4)
            new_position = (random.choice(valuesX[x_start:x_end]),random.choice(valuesY[y_start:y_end]))
        if new_position in graph or Graph.in_obstacle(environment_grid,new_position,robot_radius):
            continue
        nearest=graph.nearest_point(new_position)

        if Graph.clear_path(environment_grid,new_position,nearest,robot_radius):
            graph[nearest][1].append(new_position)
            if new_position not in graph:
                graph[new_position]=[0,[]]
                graph['parents'][new_position] = nearest
            graph[new_position][1].append(nearest)

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
    start=(20,20)
    end=(28,28)
    radius=.5
    graph, path =plan_path(start,end,radius,grid, 2000,20)
    graph.showGraph(path, ax)
    #print(graph)
    print(path)