import matplotlib.pyplot as plt
import numpy as np
import random
import statistics
import sys

from numpy.lib.function_base import median
sys.setrecursionlimit(10000)

treeVisualizationList = []

class rangeTree:

    def __init__(self, data):
        
        self.initialData = data

        max = np.max(self.initialData, axis=1).tolist()
        min = np.min(self.initialData, axis=1).tolist()

        plt.scatter(max, min, marker='x')
        plt.suptitle('Data Visualization')
        #plt.show()

        dataList = []

        for item in range(len(max)):
            dataList.append([max[item],min[item]])

        self.data = dataList
        self.depth = 0



    def rangeTreeDivision(self, subtree=[-1,-1,-1], coordinates = True, depth = 0):

            
        if subtree == [-1,-1,-1]:
            dataList = self.data
        else:
            dataList = subtree


        if len(dataList) <= 2:

            return {
                'subtree' : dataList,
                'depth' : depth,
            }

        else:
            pass

        
        leftSubtree,rightSubtree = ([] for i in range(2))

        if coordinates == True:
            currentCoordinate = 0
        else:
            currentCoordinate = 1
            
        coordinates = not coordinates

        dataToDivide = []

        for item in dataList:
            dataToDivide.append(item[currentCoordinate])
        
        medianNum = statistics.median(dataToDivide)

                

        for subtree in dataList:
            if subtree[currentCoordinate] < medianNum:
                leftSubtree.append(subtree)
            else:
                rightSubtree.append(subtree)

                    

        for subtree in [leftSubtree,rightSubtree]:
            depth = depth+1
            treeVisualizationList.append(self.rangeTreeDivision(subtree,coordinates,depth))
        
        return treeVisualizationList


    def findNearestNeighbors(self,point):

        nearestNeighbors = []

        initialData = self.initialData
        treeData = self.initialData
        treeData.append(point)

        sampleTree__ = rangeTree(treeData)

        treeData = sampleTree__.data
            

        treeQueryData = self.rangeTreeDivision(treeData)

        for subtree in range(len(treeQueryData)):
            try:
                for x in treeQueryData[subtree]['subtree']:
                    if x == treeData[-1]:

                        for x in treeQueryData[subtree]['subtree']:
                            if x != treeData[-1]:
                                nearestNeighbors.append(x)
                                
                        for neighborCounter in range(3):

                            if not nearestNeighbors:
                                for x in treeQueryData[subtree-neighborCounter]['subtree']:
                                    if x != treeData[-1]:
                                        nearestNeighbors.append(x)


                                for x in treeQueryData[subtree+neighborCounter]['subtree']:
                                    if x != treeData[-1]:
                                        nearestNeighbors.append(x)
                                    
                            if not nearestNeighbors:

                                for x in treeQueryData[neighborCounter]['subtree']:
                                    if x != treeData[-1]:
                                        nearestNeighbors.append(x)

                                                        
            except:
                pass
                
        nearestNeighborsList = []

        for item in nearestNeighbors:
            nearestNeighborsList.append(initialData[treeData.index(item)])

        return nearestNeighborsList



"""
counter = 0

data = []

for x in range(100):
    tempList = []
    for y in range(5):
        tempList.append(random.randint(1, 500))
    data.append(tempList)

treeVisualizationList = []
sampleTree = rangeTree(data)
nearestNeighbors = sampleTree.findNearestNeighbors([400,105,105,435,125])
        
if bool(nearestNeighbors) == False:        
    counter+=1
else:
    print(nearestNeighbors)
    pass

    """