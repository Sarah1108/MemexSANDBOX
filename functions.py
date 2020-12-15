#############################
# STORING FUNCTIONS #########
#############################

import os
import PyPDF2
import yaml 
import re
import pdf2image, pytesseract
import json

# generate path from bibtex code:
def generatePublPath(pathToMemex, bibTexCode):
    temp = bibTexCode.lower()
    directory = os.path.join(pathToMemex, temp[0], temp[:2], bibTexCode)
    return(directory)

#reuse the bibload function
def loadBib(bibTexFile):

    bibDic = {}
    recordsNeedFixing = []

    with open(bibTexFile, "r", encoding="utf8") as f1:
        records = f1.read().split("\n@")

        for record in records[1:]:
            # let process ONLY those records that have PDFs
            if ".pdf" in record.lower():
                completeRecord = "\n@" + record

                record = record.strip().split("\n")[:-1]

                rType = record[0].split("{")[0].strip()
                rCite = record[0].split("{")[1].strip().replace(",", "")

                bibDic[rCite] = {}
                bibDic[rCite]["rCite"] = rCite
                bibDic[rCite]["rType"] = rType
                bibDic[rCite]["complete"] = completeRecord

                for r in record[1:]:
                    key = r.split("=")[0].strip()
                    val = r.split("=")[1].strip()
                    val = re.sub("^\{|\},?", "", val)

                    bibDic[rCite][key] = val

                    # fix the path to PDF
                    if key == "file":
                        if ";" in val:
                            #print(val)
                            temp = val.split(";")

                            for t in temp:
                                if t.endswith(".pdf"):
                                    val = t

                            bibDic[rCite][key] = val

    print("="*80)
    print("NUMBER OF RECORDS IN BIBLIGORAPHY: %d" % len(bibDic))
    print("="*80)
    return(bibDic)

def generatePageLinks(pNumList):
    listMod = ["DETAILS"]
    listMod.extend(pNumList)

    toc = []
    for l in listMod:
        toc.append('<a href="%s.html">%s</a>' % (l, l))
    toc = " ".join(toc)

    pageDic = {}
    for l in listMod:
        pageDic[l] = toc.replace('>%s<' % l, ' style="color: red;">%s<' % l)

    return(pageDic)
#prettifyBib

def prettifyBib(bibText):
    bibText = bibText.replace("{{", "").replace("}}", "")
    bibText = re.sub(r"\n\s+file = [^\n]+", "", bibText)
    bibText = re.sub(r"\n\s+abstract = [^\n]+", "", bibText)
    return(bibText)

def dicOfRelevantFiles(pathToMemex, extension):
    dic = {}
    for subdir, dirs, files in os.walk(pathToMemex):
        for file in files:
            # process publication tf data
            if file.endswith(extension):
                key = file.replace(extension, "")
                value = os.path.join(subdir, file)
                dic[key] = value
    return(dic)

def ocrPublication(pathToMemex, citationKey, language):
    publPath = generatePublPath(pathToMemex, citationKey)    
    pdfFile  = os.path.join(publPath, citationKey + ".pdf")
    jsonFile = os.path.join(publPath, citationKey + ".json")
    saveToPath = os.path.join(publPath, "pages")

    pdfFileTemp= removeCommentsFromPDF(pdfFile) 


    if pdfFileTemp != False:

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
    else:
        print("="*80)
        print("Something wrong with the file")
        print("="*80)

def removeCommentsFromPDF(pathToPdf):
    with open(pathToPdf, 'rb') as pdf_obj:
        pdf = PyPDF2.PdfFileReader(pdf_obj)
        out = PyPDF2.PdfFileWriter()
        for page in pdf.pages:
            out.addPage(page)
            out.removeLinks()
        tempPDF = pathToPdf.replace(".pdf", "_TEMP.pdf")
        with open(tempPDF, 'wb') as f: 
            out.write(f)
    return(tempPDF)

def identifyLanguage(bibRecDict, fallBackLanguage):
    if "langid" in bibRecDict:
        try:
            language = langKeys[bibRecDict["langid"]]
            message = "\t>> Language has been successfuly identified: %s" % language
        except:
            message = "\t>> Language ID `%s` cannot be understood by Tesseract; fix it and retry\n" % bibRecDict["langid"]
            message += "\t>> For now, trying `%s`..." % fallBackLanguage
            language = fallBackLanguage
    else:
        message = "\t>> No data on the language of the publication"
        message += "\t>> For now, trying `%s`..." % fallBackLanguage
        language = fallBackLanguage
    print(message)
    return(language)