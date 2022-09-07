import io

import numpy as np 
import pandas as pd 
import re
import time
from random import shuffle
from sklearn.metrics.pairwise import cosine_similarity,cosine_distances
from numpy import dot
from numpy.linalg import norm
from scipy import spatial
from importArticles import articlesDataframe
from datasketch import MinHash, MinHashLSHForest


#Preprocess will split a string of text into individual tokens/shingles based on whitespace.
def preprocess(text):
    text = re.sub(r'[^\w\s]','',text)
    tokens = text.lower()
    tokens = tokens.split()
    return tokens

#Number of Permutations
permutations = 128

#Number of Recommendations to return
num_recommendations = 10

def get_forest(data, perms):
    start_time = time.time()
    
    minhash = []
    
    for text in data['title']:
        tokens = preprocess(text)
        m = MinHash(num_perm=perms)
        for s in tokens:
            m.update(s.encode('utf8'))
        minhash.append(m)
        
    forest = MinHashLSHForest(num_perm=perms)
    
    for i,m in enumerate(minhash):
        forest.add(i,m)
        
    forest.index()
    
    print('It took %s seconds to build forest.' %(time.time()-start_time))
    
    return forest

def predict(text, database, perms, num_results, forest):
    start_time = time.time()
    
    tokens = preprocess(text)
    m = MinHash(num_perm=perms)
    for s in tokens:
        m.update(s.encode('utf8'))
        
    idx_array = np.array(forest.query(m, num_results))
    if len(idx_array) == 0:
        return None # if your query is empty, return none
    
    #result = database.iloc[idx_array]['title']
    results =pd.DataFrame(database.iloc[idx_array]['title'])

    
    
    print('It took %s seconds to query forest.' %(time.time()-start_time))
    
    return results



db = articlesDataframe 
print(db)
forest = get_forest(db,permutations)
num_recommendations = len(articlesDataframe)
title = 'Earnings and revenue expectations for E'
result = predict(title,db, permutations, num_recommendations, forest)

print(result)
list =[]

list.append(result['title'].values.tolist())       
sims = []
for j in range(len(list)):
    for i in range(len(list[j])):
        a = set(title)
        b = set(list[j][i]) 
        sim = float(len(a.intersection(b))) / len(a.union(b))
        sims.append(sim)

similarity = pd.DataFrame(sims)
similarity.columns = ['Similarity']
print(similarity)

results = pd.concat([result, similarity], axis=1, join='inner')
print('\n Top Recommendation(s) is(are): \n',results)