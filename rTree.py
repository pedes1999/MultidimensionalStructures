import matplotlib.pyplot as plt
import numpy as np
import random

from numpy.lib.function_base import median
import sys
from sklearn import tree

from sklearn.exceptions import DataDimensionalityWarning
sys.setrecursionlimit(10000)

treeVisualizationList=[]


QTREE_VARIABLE = 4

class rTree:

    def __init__(self,data):
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

    def rTreeSubdivision(self,dataList,depth = 0,rtreeDimensions = [0,0]):

        parentSubtree = dataList

        if len(dataList) <= QTREE_VARIABLE:
            
            return {
                    'subtree' : dataList,
                    'depth' : depth,
                    'RTree Dimensions' : rtreeDimensions
                }

        else:
            pass


        x1,x2,x3,x4 = ([] for i in range(4))

        
        
        rTreeSubdivisionHeight = min(x[0] for x in dataList)
        rTreeSubdivisionHeight_ = max(x[0] for x in dataList)
        rTreeSubdivisionWidth = min(x[1] for x in dataList)
        rTreeSubdivisionWidth_ = max(x[1] for x in dataList)


        rTreeDecisionWidth = (rTreeSubdivisionWidth+rTreeSubdivisionWidth_)/2
        rTreeDecisionHeight = (rTreeSubdivisionHeight+rTreeSubdivisionHeight_)/2

        dimensions = [rTreeDecisionHeight,rTreeDecisionWidth]
        for item in dataList:

            if item[0] > dimensions[0] and item[1] > dimensions[1]:
                x1.append(item)
            elif item[0] > dimensions[0] and item[1] < dimensions[1]:
                x2.append(item)
            elif item[0] < dimensions[0] and item[1] < dimensions[1]:
                x3.append(item)
            else:
                x4.append(item)

        

        for subtree in [x1,x2,x3,x4]:
            depth = depth+1
            treeVisualizationList.append(self.rTreeSubdivision(subtree,depth,dimensions))

        return treeVisualizationList
        
    def findNearestNeighbors(self,point):

        nearestNeighbors = []

        initialData = self.initialData
        treeData = self.initialData
        treeData.append(point)

        sampleTree__ = rTree(treeData)

        treeData = sampleTree__.data
        

        treeQueryData = self.rTreeSubdivision(treeData)

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
            try:
                nearestNeighborsList.append(initialData[treeData.index(item)])
            except:
                pass

        return nearestNeighborsList
