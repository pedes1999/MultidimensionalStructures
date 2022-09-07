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
#from listFiles import *
from collections import Counter
from nltk.stem import PorterStemmer 
import traceback

closedClassTags = ['CD', 'CC', 'DT', 'EX', 'IN', 'LS', "''", ',', '.', '``', 'MD', 'PDT', 'POS', 'PRP', 'PRP$', 'RP', 'TO', 'UH', 'WDT', 'WP', 'WP$', 'WRB']

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
    f = open(tempArticlePath, 'r')
    eris = f.read()
    lines = []
    for line in eris:
        if line in ['\n', '\r\n']:
            break
    for line in f:
        lines.append(line)
    tempArticle = "".join(lines)
    tokens = nltk.word_tokenize(eris)
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


def computeTF(articlePath):
    tfDictionary = {}
    tempArticleTokenized = tokenization(articlePath)
    wordsLength = tempArticleTokenized[2]
    bagOfWords = tempArticleTokenized[1]
    for x in bagOfWords:
        tempNum = x[1] / float(wordsLength)
        tfDictionary[x[0]] = format(tempNum, '.6f')
    return tfDictionary



#wordsDict = {}


def computeIDF():
    wordsDict = {}
    counter3=0
    documents = []
    concPaths_ = listConcatTextsCollE()
    for x in concPaths_:
        f = open(x, "r")
        documents.append(f.read())
    n = len(documents)
    for x in documents:
        tempBagofWords=x.split(' ')
        for word in tempBagofWords:
            try:
                wordsDict[word] +=1
            except:
                wordsDict[word] = 1
    erCount = 0
    wordsToRemove = []
    for word, val in wordsDict.items():
        try:
            numToDict = math.log(n/float(val))
            wordsDict[word] = format(numToDict, '.5f')
        except:
            wordsToRemove.append(word)
    for word in wordsToRemove:
        del wordsDict[word]
    return wordsDict


idfs = computeIDF()

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
