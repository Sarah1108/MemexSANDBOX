import PyPDF2
import functions
import yaml
import os
import json


settingsFile = "./settings.yml"
settings = yaml.safe_load(open(settingsFile))

memexPath = settings["path_to_memex"]

pathToMemex = memexPath #"pathToMemex"
citationKey = "alexanderShouldLiberalArts2012"

publPath = functions.generatePublPath(pathToMemex, citationKey)
#pathToPdf = settings["path_to_pdf"]
pathToPdf = os.path.join(publPath, "\\", citationKey, ".pdf")# um den Pfad zum PDF zu finden
#pdfFileDST = os.path.join(tempPath, "%s.pdf" % bibRecDict["rCite"])

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
