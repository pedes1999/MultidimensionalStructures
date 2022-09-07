from importArticles import *
from sklearn.model_selection import train_test_split
from kdTree import *
import time
from LSH import *
from quadTree import *
from rangeTree import *
from rTree import *

sys.setrecursionlimit(10000)
df = articlesDataframeFinal

trainDf, testDf = train_test_split(df, test_size=0.1)

print('Executing KD Tree, Quad Tree, Range Tree, R Tree functions using data from',len(df),'articles')
time.sleep(0.5)
print('Data has been split to',len(trainDf),'train articles to be added to Trees and',len(testDf),'articles for queries')
time.sleep(0.5)

print('----------------------------KD Tree Demo----------------------------')

try:
    start_time = time.time()

    col_one_list = trainDf['vectors'].tolist()

    kdTreeDemo = kdTree(col_one_list)

    timeElapsed = time.time() - start_time

    print(timeElapsed,"seconds elapsed to insert",len(trainDf),"train articles to KD Tree. Average insertion time:",(timeElapsed/len(trainDf)))

    KdTreeInsertionTime = timeElapsed

    rowToQuery = testDf.sample()

    print('Randomly selected article:\n',rowToQuery.iloc[0]['description'])


    closestNeighbor = kdTreeClosest(kdTreeDemo,rowToQuery['vectors'].tolist()[0])

    print("The article's vector is",rowToQuery['vectors'].tolist()[0])
    print("Using KD Tree, its nearest neighbor is ",closestNeighbor)

    tempList = trainDf['vectors'].tolist()

    for item in range(len(tempList)):
        if tempList[item] == closestNeighbor:
            itemToPick = item

    matchedText = trainDf.iloc[itemToPick]['description']

    print('Closest neighbor to use for category classification, according to KD Tree, is:')
    print(matchedText)

    KdtreeLSH = lshSimilarity(rowToQuery.iloc[0]['description'],matchedText)

    print('LSH Similartiy:',KdtreeLSH)
except:
    pass
time.sleep(0.5)

print('----------------------------KD Tree Demo End----------------------------')

input("Press Enter for Quad Tree Demo...")

print('----------------------------Quad Tree Demo----------------------------')
try:
    start_time = time.time()

    col_one_list = trainDf['vectors'].tolist()

    quadTreeDemo = quadTree(col_one_list)

    timeElapsed = time.time() - start_time

    print(timeElapsed,"seconds elapsed to insert",len(trainDf),"train articles to KD Tree. Average insertion time:",(timeElapsed/len(trainDf)))

    quadTreeInsertionTime = timeElapsed

    rowToQuery = testDf.sample()

    print('Randomly selected article:\n',rowToQuery.iloc[0]['description'])
    nearestNeighbors = quadTreeDemo.findNearestNeighbors(rowToQuery['vectors'].tolist()[0])

    print("The article's vector is",rowToQuery['vectors'].tolist()[0])
    print("Using Quad Tree, its nearest neighbor list is:",nearestNeighbors)

    tempList = trainDf['vectors'].tolist()

    newsIndexes = []

    for item in nearestNeighbors:
        for item_ in range(len(tempList)):
            if tempList[item_] == item:
                newsIndexes.append(item_)

    print('Closest neighbors to use for category classification, according to Quad Tree, are:')

    for item in newsIndexes:
        matchedText = trainDf.iloc[item]['description']
        print(matchedText)
        print('LSH Similartiy:',lshSimilarity(rowToQuery.iloc[0]['description'],matchedText))
    
    quadTreeSimilarity  = lshSimilarity(rowToQuery.iloc[0]['description'],matchedText)
except:
    pass

print('----------------------------Quad Tree Demo End----------------------------')

input("Press Enter for Range Tree Demo...")

print('----------------------------Range Tree Demo----------------------------')
try:
    start_time = time.time()

    col_one_list = trainDf['vectors'].tolist()

    rangeTreeDemo = rangeTree(col_one_list)

    timeElapsed = time.time() - start_time

    print(timeElapsed,"seconds elapsed to insert",len(trainDf),"train articles to KD Tree. Average insertion time:",(timeElapsed/len(trainDf)))

    rangeTreeTime = timeElapsed

    rowToQuery = testDf.sample()

    print('Randomly selected article:\n',rowToQuery.iloc[0]['description'])
    nearestNeighbors = rangeTreeDemo.findNearestNeighbors(rowToQuery['vectors'].tolist()[0])

    print("The article's vector is",rowToQuery['vectors'].tolist()[0])
    print("Using Range Tree, its nearest neighbor list is:",nearestNeighbors)

    tempList = trainDf['vectors'].tolist()

    newsIndexes = []

    for item in nearestNeighbors:
        for item_ in range(len(tempList)):
            if tempList[item_] == item:
                newsIndexes.append(item_)

    print('Closest neighbors to use for category classification, according to Range Tree, are:')

    for item in newsIndexes:
        matchedText = trainDf.iloc[item]['description']
        print(matchedText)
        print('LSH Similartiy:',lshSimilarity(rowToQuery.iloc[0]['description'],matchedText))
    
    rangeTreeSimilarity = lshSimilarity(rowToQuery.iloc[0]['description'],matchedText)
except:
    pass
input("Press Enter for R Tree Demo...")

print('----------------------------R Tree Demo----------------------------')
try:
    start_time = time.time()

    col_one_list = trainDf['vectors'].tolist()

    rTreeDemo = rTree(col_one_list)

    timeElapsed = time.time() - start_time

    print(timeElapsed,"seconds elapsed to insert",len(trainDf),"train articles to KD Tree. Average insertion time:",(timeElapsed/len(trainDf)))

    rTreeInsertionTime = timeElapsed
    rowToQuery = testDf.sample()

    print('Randomly selected article:\n',rowToQuery.iloc[0]['description'])
    nearestNeighbors = rTreeDemo.findNearestNeighbors(rowToQuery['vectors'].tolist()[0])
    print("The article's vector is",rowToQuery['vectors'].tolist()[0])
    print("Using R Tree, its nearest neighbor list is:",nearestNeighbors)

    tempList = trainDf['vectors'].tolist()

    newsIndexes = []

    for item in nearestNeighbors:
        for item_ in range(len(tempList)):
            if tempList[item_] == item:
                newsIndexes.append(item_)

    print('Closest neighbors to use for category classification, according to Quad Tree, are:')

    for item in newsIndexes:
        matchedText = trainDf.iloc[item]['description']
        print(matchedText)
        print('LSH Similartiy:',lshSimilarity(rowToQuery.iloc[0]['description'],matchedText))
    
    rTreeSimilarity = lshSimilarity(rowToQuery.iloc[0]['description'],matchedText)
except:
    pass

names = ['KD Tree', 'Quad Tree', 'Range Tree','R Tree']

timesList = [KdTreeInsertionTime,quadTreeInsertionTime,rangeTreeTime,rTreeInsertionTime]
LSHList = [KdtreeLSH,quadTreeSimilarity,rangeTreeSimilarity,rTreeSimilarity]

plt.show()
plt.figure(figsize=(9, 3))

plt.subplot(131)
plt.bar(names, timesList)
plt.suptitle('Total Insert Time in every Tree')

plt.show()

plt.figure(figsize=(9, 3))

plt.subplot(131)
plt.bar(names, LSHList)
plt.suptitle('Average Similarity for every Tree')

plt.show()
