from graph import Graph

if __name__=="__main__":
    env = Graph.createEnvironment("environments/environment5.txt")
    Graph.displayEnvironment(env)
    test=Graph.occupancyGrid(env)
    print(test)
    Graph.displayGrid(test)
    print(test.shape)