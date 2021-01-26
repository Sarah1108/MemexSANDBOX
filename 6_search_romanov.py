import re, os, yaml, json, random
from datetime import datetime

# SCRIPT WITH OUR PREVIOUS FUNCTIONS
import functions ## load functions

###########################################################
# VARIABLES ###############################################
###########################################################

settings = functions.loadYmlSettings("settings.yml") ###define settingsfile

###########################################################
# FUNCTIONS ###############################################
###########################################################

def searchOCRresults(pathToMemex, searchString):
    print("SEARCHING FOR: `%s`" % searchString)
    files = functions.dicOfRelevantFiles(pathToMemex, ".json") ##load all jsonfiles
    results = {} ##create empty dictionary

    for citationKey, pathToJSON in files.items():
        data = json.load(open(pathToJSON,"r", encoding="UTF8"))###changend by adding "r" and encoding="UTF8"
        #print(citationKey)
        count = 0 # set counter

        for pageNumber, pageText in data.items():   ###loop through each json
            if re.search(r"\b%s\b" % searchString, pageText, flags=re.IGNORECASE): ###if searchString in there 
                if citationKey not in results: # if citekey is not in the results add to dictionary
                    results[citationKey] = {}

                # relative path
                a = citationKey.lower() # build path 
                relPath = os.path.join(a[:1], a[:2], citationKey, "pages", "%s.html" % pageNumber) ##create path to .html with citekey and first/second letter
                countM = len(re.findall(r"\b%s\b" % searchString, pageText, flags=re.IGNORECASE)) ## count matches
                pageWithHighlights = re.sub(r"\b(%s)\b" % searchString, r"<span class='searchResult'>\1</span>", pageText, flags=re.IGNORECASE) ##ad page text containing results 

                results[citationKey][pageNumber] = {}
                results[citationKey][pageNumber]["pathToPage"] = relPath
                results[citationKey][pageNumber]["matches"] = countM
                results[citationKey][pageNumber]["result"] = pageWithHighlights.replace("\n", "<br>")

                count  += 1 ##ad to conter

        if count > 0: ### if there are search results print the citekey
            print("\t", citationKey, " : ", count)
            newKey = "%09d::::%s" % (count, citationKey)
            results[newKey] = results.pop(citationKey)

            # add time stamp
            currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            results["timestamp"] = currentTime ## save time stamp in dicitionary
            # add search string (as submitted)
            results["searchString"] = searchString ##save searchstring in dictionary

    saveWith = re.sub("\W+", "", searchString) 
    saveTo = os.path.join(pathToMemex, "searches", "%s.searchResults" % saveWith) #create path to safe
    with open(saveTo, 'w', encoding='utf8') as f9c: # save into json
        json.dump(results, f9c, sort_keys=True, indent=4, ensure_ascii=False)

###########################################################
# RUN THE MAIN CODE #######################################
###########################################################

#searchPhrase  = r"corpus\W*based"
#searchPhrase  = r"corpus\W*driven"
#searchPhrase  = r"multi\W*verse"
#searchPhrase  = r"text does ?n[o\W]t exist"
#searchPhrase  = r"corpus-?based"

searchOCRresults(settings["path_to_memex"], "digital")
#exec(open("9_Interface_IndexPage.py").read())