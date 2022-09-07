import pandas as pd
import nltk
import json
from collections import Counter
from nltk.stem import PorterStemmer 
import traceback
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import openpyxl
import math
import pickle
import nltk
import json
from collections import Counter
from nltk.stem import PorterStemmer 
import traceback
from progress.bar import FillingSquaresBar
import numpy as np

df = pd.read_csv('articles_data.csv')

articlesDataframe = df[['source_name','author','title','description']]

articlesDataframe.dropna(inplace=True)

articlesDataframe = articlesDataframe.head(2000)
closedClassTags = ['CD', 'CC', 'DT', 'EX', 'IN', 'LS', "''", ',', '.', '``', 'MD', 'PDT', 'POS', 'PRP', 'PRP$', 'RP', 'TO', 'UH', 'WDT', 'WP', 'WP$', 'WRB']
ps = PorterStemmer()


def listToString(test_list):  
    res = str(test_list).strip('[]')
    return res


def tokenizedPreprocessor(NTLKList):
    tempFinalList = []
    wordsList = []
    for x in NTLKList:
        if x[1] in closedClassTags:
            pass
        else:
            tempFinalList.append(x)
    for x in tempFinalList:
        wordsList.append(x[0])
    counts = Counter(wordsList)
    your_list = [list(i) for i in counts.items()]

    return [tempFinalList,your_list]

def tokenization(tempArticlePath):

    tokens = nltk.word_tokenize(tempArticlePath)
    tempTokenizedArticleList = nltk.pos_tag(tokens)
    preprocessedFunctionReturn = tokenizedPreprocessor(tempTokenizedArticleList)
    tempTokenizedArticle = preprocessedFunctionReturn[0]
    totalLemmaArticleCount = preprocessedFunctionReturn[1]
    signigicantWordCount = len(tempTokenizedArticleList)
    ps = PorterStemmer()
    for item in totalLemmaArticleCount:
        item[0] = ps.stem(item[0])
    res = {}
    for sub in totalLemmaArticleCount:
        try:
            res.update({sub[0]: res.get(sub[0]) + sub[1]})
        except:
            res[sub[0]] = sub[1]
    totalLemmaArticleCount = []
    for key,value in res.items():
        totalLemmaArticleCount.append([key,value])
    return [tempTokenizedArticle,totalLemmaArticleCount,signigicantWordCount]

def computeIDF(df,column):
    
    wordsDict = {}
    documents = df[column]
    n = len(documents)
    for x in documents:
        tempBagofWords=x.split(' ')
        for word in tempBagofWords:
            word = ps.stem(word)
            try:
                if word[-1] in ['.',',','?','-','+','=',"'",'`']:
                    word = word[:-1]
            except:
                pass
            try:
                wordsDict[word] += 1
            except:
                wordsDict[word] = 1
    erCount = 0
    wordsToRemove = []
    for word, val in wordsDict.items():
        try:
            numToDict = math.log(n/val)
            wordsDict[word] = float(format(numToDict, '.5f'))
        except:
            wordsToRemove.append(word)
    wordsToRemove.append('—')
    for word in wordsToRemove:
        try:
            del wordsDict[word]
        except:
            pass
    return wordsDict



eris = computeIDF(articlesDataframe,'description')

def computeTF(articlePath):
    tfDictionary = {}
    tempArticleTokenized = tokenization(articlePath)
    wordsLength = tempArticleTokenized[2]
    bagOfWords = tempArticleTokenized[1]
    for x in bagOfWords:
        tempNum = x[1] / float(wordsLength)
        tfDictionary[x[0]] = format(tempNum, '.6f')
    return tfDictionary

def computeTFIDF(articlePath,idfs):
    tfidf = {}
    tfBagOfWords = computeTF(articlePath)
    for word,val in tfBagOfWords.items():
        try:
            tempNum = float(val)*float(idfs[word])+0.3
            tfidf[word] = float(format(tempNum, '.5f'))
        except:
            pass
    return tfidf


cou = 0


df = pd.DataFrame(eris.items(), columns=['Word', 'IDF'])
df = df.sort_values(by=['IDF'])
tokensList = df['Word'].tolist()

vectorsColumn = []

bar2 = FillingSquaresBar("Processing", max=len(articlesDataframe['description']),suffix = "Users Calculated: %(index)d/%(max)d  Estimated Time Remaining: %(eta_td)s ")

for x in articlesDataframe['description']:

    vectorList = []

    cou += 1

    tfIdfForArticle = computeTFIDF(x,eris)

    for key,value in tfIdfForArticle.items():
        vectorList.append(int(tokensList.index(key)*value*1000))
    try:
        vectorsColumn.append(vectorList[:10])
    except:
        pass

    bar2.next()


articlesDataframe['vectors'] = vectorsColumn

output = []
falseNegative = []

for x in range(len(vectorsColumn)):
    if vectorsColumn[x] not in output:
        output.append(vectorsColumn[x])
    else:
        falseNegative.append(x)



    

"""


def try_join(l):

    try:
        return ','.join(map(str, l))
    except TypeError:
        return np.nan

articlesDataframe['liststring'] = [try_join(l) for l in articlesDataframe['vectors']]

print(articlesDataframe)

articlesDataframe.drop_duplicates(subset=['liststring'])





articlesDataframe = articlesDataframe.truncate(before=0, after=len(vectorsColumn)-len(falseNegative)-2)

print(len(falseNegative))
"""
articlesDataframe = articlesDataframe.reset_index()

articlesDataframe.drop(falseNegative, inplace=True)



articlesDataframeFinal = articlesDataframe.drop(articlesDataframe[articlesDataframe.vectors.map(len) < 10].index)


