from graph import Graph
import numpy as np
import random

def plan_path(start_point,end_point,robot_radius,environment_grid):
    graph=Graph()
    graph[start_point]=[]
    grid_shape=environment_grid.shape
    valuesX=np.linspace(0,grid_shape[0]/4,grid_shape[0]+1)
    valuesY=np.linspace(0,grid_shape[1]/4,grid_shape[1]+1)
    while len(graph)<500:
        new_position = (random.choice(valuesX),random.choice(valuesY))
        if Graph.in_obstacle(environment_grid,new_position,robot_radius):
            continue
        nearest=graph.nearest_point(new_position)
        #You can clean/change some of these methods if needed
        if Graph.clear_path(environment_grid,new_position,nearest,robot_radius):
            graph[nearest].append(new_position)
            if new_position not in graph:
                graph[new_position]=[]
            graph[new_position].append(nearest)
            #
            #add the parent thing
            #
    return graph

if __name__=="__main__":
    env = Graph.createEnvironment("environments/environment5.txt")
    grid=Graph.occupancyGrid(env)
    start=(1,1)
    end=(28,28)
    radius=.5
    graph =plan_path(start,end,radius,grid)
    print(graph)