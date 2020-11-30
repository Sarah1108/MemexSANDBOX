# ocr-ing pdf
import os, json
import pdf2image, pytesseract
import functions 
import yaml
import removeComments
### variables
settingsFile = "./settings.yml"
settings = yaml.safe_load(open(settingsFile))
memexPath = settings["path_to_memex"]
language = settings["language_keys"]
#def findLanguage(language):               
                                             ### check if language in file if yes, take for ocr-ing: language = tempLang
                                             ### if not change to value in language_key yaml file (en-eng for example) language = val
                                             ### else function - print tempLang, stop function - add manually to yaml file, 
                                             ### else no language - take default language; language = eng 
 ############

def checkLangId(record):                   
    languages = yaml.safe_load(open(language))   #loads the languages from the yaml file

    try:    #if there is no key = language it will crash otherwise 
        if record["langid"] in languages:        #if the language is in the yaml file
            tempLang = languages[record["langid"]]   #take the proper OCR abreviation for the language
        elif record["langid"] not in languages:      #if not print a warning
            print(record["langid"]+"is not in the "+language+"file, please add. Will try with english as default")
            tempLang = "eng"
        else:   #default = eng
            tempLang = "eng" #default
    except:  #if there is no key = language set tempLang to eng
        tempLang = "eng" #default
        
    return tempLang

def ocrPublication(pathToMemex, citationKey, language): 
    publPath = functions.generatePublPath(memexPath, citationKey)
    pdfFile  = os.path.join(publPath, citationKey + ".pdf")
    jsonFile = os.path.join(publPath, citationKey + ".json")
    saveToPath = os.path.join(publPath, "pages")
    pdfFileTemp= removeComments.removeCommentsFromPDF(pdfFile)     
    if not os.path.isfile(jsonFile):
        if not os.path.exists(saveToPath):
            os.makedirs(saveToPath)
        print("\t>>> OCR-ing: %s" % citationKey)
        textResults = {}
        images = pdf2image.convert_from_path(pdfFileTemp)
        pageTotal = len(images)
        pageCount = 1
        for image in images:
            image = image.convert('1')
            finalPath = os.path.join(saveToPath, "%04d.png" % pageCount)
            image.save(finalPath, optimize=True, quality=10)
            text = pytesseract.image_to_string(image, lang=language)
            textResults["%04d" % pageCount] = text
            print("\t\t%04d/%04d pages" % (pageCount, pageTotal))
            pageCount += 1
        with open(jsonFile, 'w', encoding='utf8') as f9:
            json.dump(textResults, f9, sort_keys=True, indent=4, ensure_ascii=False)
    else:
        print("\t>>> %s has already been OCR-ed..." % citationKey)
    os.remove(pdfFileTemp)

################
## ALL FILES ###
################    
def processAllFiles(pathToMemex):

    bibData = functions.loadBib(settings["bib_all"]) #loads the bib file
    
    for k,v in bibData.items():        
        language = checkLangId(v)

    ocrPublication(pathToMemex, k, language)

processAllFiles(memexPath)

print("Done!")