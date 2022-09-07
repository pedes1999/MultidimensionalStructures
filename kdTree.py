import math
import collections
import operator
import sys
import random
from statistics import median
sys.setrecursionlimit(10000)

def distance(point1,point2):

    if len(point1) == len(point2):
        tempDistanceAxes = []
        squaresSum = 0

        for x in range(len(point1)):
            tempDistanceAxes.append(point1[x]-point2[x])

        for item in tempDistanceAxes:
            squaresSum+=item*item

        return math.sqrt(squaresSum)

    else:

        print("Points",point1,point2,"of unequal length")
        
def closestNeighbor(pointsData, newPoint):
    closestPoint = None
    minDistance = None

    for point in pointsData:
        currentDistance = distance(newPoint, point)

        if minDistance == None or currentDistance < minDistance:
            minDistance = currentDistance
            closestPoint = point

    print(closestPoint)
    print(minDistance)

def minDistance(point,point1,point2):
    if point1 is None:
        return point2

    if point2 is None:
        return point1

    distance1 = distance(point,point1)
    distance2 = distance(point,point2)

    if distance1 < distance2:
        return point1
    else:
        return point2

preset =  3


def checkLength(pointsData):
    individualLength = len(pointsData[0])
    

    for element in pointsData:
        if len(element) != individualLength:
            print('Points of unequal length')
            sys.exit()
    
    print('Building KD Tree with point length:',individualLength)


def kdTree(pointsData, depth=0):

    length_ = len(pointsData)

    if length_ <= 0:
        return None
    
    axis = depth % preset

    sortedPoints = sorted(pointsData, key=lambda point: point[axis])


    tempLength = int(length_/2)
    return {
        'depth' : depth+1,
        'point': sortedPoints[tempLength],
        'left_tree': kdTree(sortedPoints[:tempLength], depth+1),
        'right_tree' : kdTree(sortedPoints[tempLength +1:], depth+1)
    }   



def kdTreeClosest(root, point, depth=0):
    if root is None:
        return None

    axis = depth % preset

    nextBranch = None
    oppositeBranch = None

    if point[axis] < root['point'][axis]:
        nextBranch = root['left_tree']
        oppositeBranch = root['right_tree']
    else:
        nextBranch = root['right_tree']
        oppositeBranch = root['left_tree']

    try:
        bestSolution = minDistance(point,kdTreeClosest(nextBranch,point,depth+1),root['point'])
    except:
        bestSolution = minDistance(point,kdTreeClosest(oppositeBranch,point,depth+1),root['point'])


    return bestSolution
    

"""

testData = [(2,4,3,7),(3,3,5,4),(3,3,5,4),(2,4,3,2),(5,12,3,9),(7,37,3,2),(24,21,42,1),(23,24,1,5),(42,4,4,1),(3,5,2,4),(72,3,3,89)]
data = []

for x in range(1200):
    tempList = []
    for y in range(4):
        tempList.append(random.randint(1, 100))
    data.append(tempList)

    
checkLength(data)
treeSample = kdTree(data)
print(kdTreeClosest(treeSample,(3,3,5,7)))
"""