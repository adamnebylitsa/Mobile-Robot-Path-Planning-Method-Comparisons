import matplotlib.pyplot as plt
import numpy as np

class Graph(dict):


    def get_path(self):
        return
    
    def nearest_point(self,point):
        nearest =None
        distance=float('inf')
        # for all the points in the graph find if the current distance is the smallest
        for k in self:
            if Graph.distance_point(point,k)<distance:
                nearest=k
                distance=Graph.distance_point(point,k)
        return nearest
    #
    #
    #
    #You can clean/change some of these methods if needed
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
        return (environment,polygon)
    
    @staticmethod
    def occupancyGrid(environment):
        grid=np.zeros([int(environment[0][0]*4),int(environment[0][1]*4)])
        for poly in environment[1]:
            minX=Graph.min_list(poly,0)
            minY=Graph.min_list(poly,1)
            maxX=Graph.max_list(poly,0)
            maxY=Graph.max_list(poly,1)
            grid[int(minX*4):int(maxX*4),int(minY*4):int(maxY*4)]=1
        return grid

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
        return 1 in grid[int(position[0]-radius*4):int(position[0]+radius*4),int(position[1]-radius*4):int(position[1]+radius*4)]
    
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