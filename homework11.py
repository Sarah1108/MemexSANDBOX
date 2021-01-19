
######import libararies
import json
import functions
import re
import yaml

settingsFile = "settings.yml"
settings = yaml.safe_load(open(settingsFile))

memexPath = settings["path_to_memex"]




def search():
    ## load OCR results
    ocrFiles = functions.dicOfRelevantFiles(memexPath, ".json")   
    citeKeys = list(ocrFiles.keys())
    word = input("Please enter a word:" )
    dicOfMatches = {}       # dictionary with citeKeys as value, matches as value
    print(ocrFiles)
    for citeKeys, word in ocrFiles.items():   
        val = json.load(open(ocrFiles[citeKeys],"r",encoding= "utf8")) # load each json file
        dicOfPages = {}
        pagenumbers = list(val.keys())
        pagetext= list(val)

        #dicOfPages[keys] = pagenumbers # didn't work
        #dicOfPages[val] = pagetext

        print(dicOfPages)

        #for pagenumbers in val:
            #if word in pagenumbers:
                

        #for word in val:
            #if word in val:
            #    dicOfMatches[citeKeys]  = word 
            #else: 
            #    dicOfMatches[citeKeys] = "notinthepage"
        #print (dicOfMatches)
   # def searchDic (dic, word):
 #   searchDic = {}    
  #  for k,v in dic.items():      # for citekeys
   #     searchDic[v]={}
    #    for key, val in v:
     #       if word in val: 
      #          searchDic[k][key] = val
    #return(searchDic)
    #searchedDic = {}
   # searchedDic = functions.searchDic(ocrFiles, word)
  #  with open("searchresults.txt", 'w', encoding='utf8') as f9:              ## save it into a textfile; avoid extension .json;
   #     json.dump(searchedDic, f9, sort_keys=True, indent=4, ensure_ascii=False)
search()