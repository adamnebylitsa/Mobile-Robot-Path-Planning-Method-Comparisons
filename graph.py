import matplotlib.pyplot as plt
import numpy as np

class Graph(dict):


    def get_path(self, start_point, end_point):
        path = [end_point]
        current_point = end_point

        while current_point != start_point:
            parent = self['parents'][current_point]
            if parent is None:
                break
            path.append(parent)
            current_point = parent
        
        path.reverse()
        print("in func: ",path)
        return path
    
    def nearest_point(self,point):
        nearest =None
        distance=float('inf')
        # for all the points in the graph find if the current distance is the smallest
        keys = list(self.keys())
        
        for k in keys:
            if k == "parents":
                continue
            if Graph.distance_point(point,k)<distance:
                nearest=k
                distance=Graph.distance_point(point,k)
        return nearest
    #
    #
    #
    #You can clean/change some of these methods if needed

    def showGraph(self, path, ax):
        keys = list(self.keys())
        for k in keys:
            if k == "parents":
                continue
            ax.plot(k[0]*4, k[1]*4, 'go')
        plt.show()
        return
    @staticmethod
    def createEnvironment(filename):
        f=open(filename,"r")
        polygon=[]
        #for each line in the file
        for x in f:
            line=x.split(" ")
            #if the first element is E 
            if line[0]=="E":
                #get the environment limits
                environment = [float(line[1]),float(line[2])]
            #if the first element is P
            elif line[0]=="P":
                #get all the points
                points=[]
                for i in range(1,len(line)):
                    temp=line[i].split(",")
                    points.append([float(temp[0]),float(temp[1])])
                polygon.append(points)
        f.close()
        print(polygon)
        return (environment,polygon)
    
    @staticmethod
    def occupancyGrid(environment, show = False):
        grid=np.zeros([int(environment[0][0]*4),int(environment[0][1]*4)])
        for poly in environment[1]:
            minX=Graph.min_list(poly,0)
            minY=Graph.min_list(poly,1)
            maxX=Graph.max_list(poly,0)
            maxY=Graph.max_list(poly,1)
            grid[int(minX*4):int(maxX*4),int(minY*4):int(maxY*4)]=1

        # grid[0][2] = 2
        # print(grid)
        
        fig, ax = plt.subplots()
        ax.imshow(grid.T, cmap='Greys', origin='lower', extent=[0, environment[0][0]*4, 0, environment[0][1]*4])
        ax.set_xlabel('X coordinate')
        ax.set_ylabel('Y coordinate')

        if show:
            ax.set_title('2D Occupancy Grid')
            plt.show()
            
        return grid, ax

    @staticmethod
    def displayGrid(grid):
        #0,0 on grid is top left corner, should not mess up any of the math just some visualization if you graph with this method
        fig = plt.figure()
        plt.imshow(grid)
        plt.show()

    @staticmethod
    def displayEnvironment(environment):
        plt.axes()
        plt.xlim(0, environment[0][0])
        plt.ylim(0,environment[0][1])
        for i in environment[1]:
            plt.gca().add_patch(plt.Polygon(i))
        plt.show()

    @staticmethod
    def max_list(lst,index):
        largest=-1*float('inf')
        for i in lst:
            if i[index]>largest:
                largest=i[index]
        return largest
    
    @staticmethod
    def min_list(lst,index):
        small=float("inf")
        for i in lst:
            if i[index]<small:
                small=i[index]
        return small
    
    @staticmethod
    def in_obstacle(grid,position,radius):
        # if 1 in grid[int((position[0]-radius)*4):int((position[0]+radius)*4),
        #                  int((position[1]-radius)*4):int((position[1]+radius)*4)]:
            # print(position)
        return 1 in grid[int((position[0]-radius)*4):int((position[0]+radius)*4),
                         int((position[1]-radius)*4):int((position[1]+radius)*4)]
    
        return 1 in grid[int(position[0]-radius*4):int(position[0]+radius*4),
                         int(position[1]-radius*4):int(position[1]+radius*4)]
    
    @staticmethod
    def clear_path(grid,point1,point2,radius):
            #get 100 points along the line and test if they are all obstacle free
        for i in range(100):
            x=point1[0]+i/100*(point2[0]-point1[0])
            y=point1[1]+i/100*(point2[1]-point1[1])
            if Graph.in_obstacle(grid,(x,y),radius):
                return False
        return True
    
    @staticmethod
    def distance_point(point1,point2):
        return((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)**.5