import os, json, yaml
import pdf2image, pytesseract
import functions
import removeComments


settingsFile = "./settings.yml"
settings = yaml.safe_load(open(settingsFile))

memexPath = settings["path_to_memex"]

pathToMemex = memexPath #"pathToMemex"


#publPath = functions.generatePublPath(pathToMemex, citationKey)
#pathToPdf = settings["path_to_pdf"]
#pathToPdf = os.path.join(publPath, "\\", citationKey, ".pdf")

def ocrPublication(pathToMemex, citationKey, language):
    citationKey = "alexanderShouldLiberalArts2012"
    publPath = functions.generatePublPath(pathToMemex, citationKey)
    pdfFile  = os.path.join(publPath, citationKey+ ".pdf")
    jsonFile = os.path.join(publPath, citationKey + ".json")
    saveToPath = os.path.join(publPath, "pages")

    pdfFileTemp = removeComments.removeCommentsFromPDF(pdfFile) # error, eventhough removeComments is working
    

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

            text = pytesseract.image_to_string(image, lang="eng")
            textResults["%04d" % pageCount] = text

            print("\t\t%04d/%04d pages" % (pageCount, pageTotal))
            pageCount += 1

        with open(jsonFile, 'w', encoding='utf8') as f9:
            json.dump(textResults, f9, sort_keys=True, indent=4, ensure_ascii=False)
    
    else:
        print("\t>>> %s has already been OCR-ed..." % citationKey)

    os.remove(pdfFileTemp)
ocrPublication("C:\\Users\\Sarah\\Documents\\Uni\\MA_DigitalHumanities\\UE_ToolsandTechniques\\MemexSANDBOX\\_data","alexanderShouldLiberalArts2012", "eng")