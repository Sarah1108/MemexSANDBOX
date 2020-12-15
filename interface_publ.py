# generate interface for the publication
#import libraries
import os, json
import pdf2image, pytesseract
import functions 
import yaml
import removeComments

### variables
settingsFile = "./settings.yml"
settings = yaml.safe_load(open(settingsFile))
memexPath = settings["path_to_memex"]

def generatePublicationInterface(citeKey, pathToBibFile):
    print("="*80)
    print(citeKey)

    #pathToBibFile = functions.dicOfRelevantFiles(memexPath, ".bib")
    #for v in pathToBibFile.items():
    #    jsonFile = v.replace(".bib", ".json")
    #return jsonFile

    print(pathToBibFile)


    jsonFile = pathToBibFile.replace(".bib", ".json")

    with open(jsonFile, encoding="utf8") as jsonData:
        ocred = json.load(jsonData)
        pNums = ocred.keys()

        pageDic = functions.generatePageLinks(pNums)

        # load page template
        with open(settings["template_page"], "r", encoding="utf8") as ft:
            template = ft.read()

        # load individual bib record
        bibFile = pathToBibFile
        bibDic = functions.loadBib(bibFile)
        bibForHTML = functions.prettifyBib(bibDic[citeKey]["complete"])

        orderedPages = list(pageDic.keys())

        for o in range(0, len(orderedPages)):
            #print(o)
            k = orderedPages[o]
            v = pageDic[orderedPages[o]]

            pageTemp = template
            pageTemp = pageTemp.replace("@PAGELINKS@", v)
            pageTemp = pageTemp.replace("@PATHTOFILE@", "")
            pageTemp = pageTemp.replace("@CITATIONKEY@", citeKey)

            if k != "DETAILS":
                mainElement = '<img src="@PAGEFILE@" width="100%" alt="">'.replace("@PAGEFILE@", "%s.png" % k)
                pageTemp = pageTemp.replace("@MAINELEMENT@", mainElement)
                pageTemp = pageTemp.replace("@OCREDCONTENT@", ocred[k].replace("\n", "<br>"))
            else:
                mainElement = bibForHTML.replace("\n", "<br> ")
                mainElement = '<div class="bib">%s</div>' % mainElement
                mainElement += '\n<img src="wordcloud.jpg" width="100%" alt="wordcloud">'
                pageTemp = pageTemp.replace("@MAINELEMENT@", mainElement)
                pageTemp = pageTemp.replace("@OCREDCONTENT@", "")

            # @NEXTPAGEHTML@ and @PREVIOUSPAGEHTML@
            if k == "DETAILS":
                nextPage = "0001.html"
                prevPage = ""
            elif k == "0001":
                nextPage = "0002.html"
                prevPage = "DETAILS.html"
            elif o == len(orderedPages)-1:
                nextPage = ""
                prevPage = orderedPages[o-1] + ".html"
            else:
                nextPage = orderedPages[o+1] + ".html"
                prevPage = orderedPages[o-1] + ".html"

            pageTemp = pageTemp.replace("@NEXTPAGEHTML@", nextPage)
            pageTemp = pageTemp.replace("@PREVIOUSPAGEHTML@", prevPage)

            pagePath = os.path.join(pathToBibFile.replace(citeKey+".bib", ""), "pages", "%s.html" % k)
            with open(pagePath, "w", encoding="utf8") as f9:
                f9.write(pageTemp)

def processAll(path_to_memex):
    pathData = functions.dicOfRelevantFiles(memexPath, ".bib")
    print(pathData)
    #bibData = functions.loadBib(settings["bib_all"])
   
    for k, v in pathData.items():
        generatePublicationInterface(k, v)

processAll(memexPath)