### import libraries

import pandas as pd
from sklearn.feature_extraction.text import (CountVectorizer, TfidfTransformer)
from sklearn.metrics.pairwise import cosine_similarity
import os, json
import pdf2image, pytesseract
import functions 
import yaml
import re
### save settings
settingsFile = "settings.yml"
settings = yaml.safe_load(open(settingsFile))
memexPath = settings["path_to_memex"]

###cload json files and create two lists

stopWFile = "stopwords.txt"
stopwordsList = open(stopWFile, "r", encoding="utf8").read().split("\n")


def generatetfidfValues():

    #dictionary with keys
    ocrFiles = functions.dicOfRelevantFiles(memexPath, ".json")
    #list with citekeys (in fixed order)
    citeKeys = list(ocrFiles.keys())

    docList   = []
    docIdList = []

    #print(ocrFiles)
    #print(citeKeys)
    #loop through list not dictionary to have sorted lists (for the corpusDic)
    for citeKey in citeKeys:
        docData = json.load(open(ocrFiles[citeKey], "r", encoding="utf8"))
        #print(docData)
    
        docId = citeKey
        doc   = " ".join(docData.values())

        doc = re.sub(r'(\w)-\n(\w)', r'\1\2', doc)
        doc = re.sub('\W+', ' ', doc)
        doc = re.sub('\d+', ' ', doc)
        doc = re.sub(' +', ' ', doc)

        docList.append(doc)
        docIdList.append(docId)
    
    #print(docList)
    #print(docIdList)
    vectorizer = CountVectorizer(ngram_range=(1,1), min_df=5, max_df=0.5, stop_words= stopwordsList)
    countVectorized = vectorizer.fit_transform(docList)
    tfidfTransformer = TfidfTransformer(smooth_idf=True, use_idf=True)
    vectorized = tfidfTransformer.fit_transform(countVectorized) # https://en.wikipedia.org/wiki/Sparse_matrix
    cosineMatrix = cosine_similarity(vectorized)

    tfidfTable = pd.DataFrame(vectorized.toarray(), index=docIdList, columns=vectorizer.get_feature_names())
    print("tfidfTable Shape: ", tfidfTable.shape) # optional
    tfidfTable = tfidfTable.transpose()
    tfidfTableDic = tfidfTable.to_dict()
    

    cosineTable = pd.DataFrame(cosineMatrix)
    print("cosineTable Shape: ", cosineTable.shape) # optional
    cosineTable.columns = docIdList
    cosineTable.index = docIdList
    cosineTableDic = cosineTable.to_dict()
    
    #create empty dictionary
    #keywordsDic = {}
    #loop through dictionary
    #for docId in tfidfTableDic:
    #    for tfIdf in value:
            #check if tfidf value is above threshold
    #        if tfIdf >= 0.05:
    #            keywordsDic= keywordsDic.keys(docId)

    filteredDic = {}
    filteredDic = functions.filterDic(tfidfTableDic, 0.05)
    with open("tfidfTableDic_filtered.txt", 'w', encoding='utf8') as f9:
        json.dump(filteredDic, f9, sort_keys=True, indent=4, ensure_ascii=False)
    
    filteredDic = {}
    filteredDic = functions.filterDic(cosineTableDic, 0.25)
    with open("cosineTableDic_filtered.txt", 'w', encoding='utf8') as f9:
        json.dump(filteredDic, f9, sort_keys=True, indent=4, ensure_ascii=False)
######Not sure how to add into new dicitionary
######Haven't found out how the key-value pairs are named in both tfidfTableDic and cosineTableDic
generatetfidfValues()
### wie heißen die Variablen? (und wie heißen die Felder mit den Werten?)