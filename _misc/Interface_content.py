import os, json
import pdf2image, pytesseract
import functions 
import yaml
import removeComments

settingsFile = "settings.yml"
settings = yaml.safe_load(open(settingsFile))

memexPath = settings["path_to_memex"]

# generate the INDEX and the CONTENTS pages
def generateMemexStartingPages(pathToMemex):
    # load index template
    with open(settings["template_index"], "r", encoding="utf8") as ft:
        template = ft.read()

    # add index.html
    with open(settings["content_index"], "r", encoding="utf8") as fi:
        indexData = fi.read()
        with open(os.path.join(pathToMemex, "index.html"), "w", encoding="utf8") as f9:
            f9.write(template.replace("@MAINCONTENT@", indexData))

    # load bibliographical data for processing
    publicationDic = {} # key = citationKey; value = recordDic

    for subdir, dirs, files in os.walk(pathToMemex):
        for file in files:
            if file.endswith(".bib"):
                pathWhereBibIs = os.path.join(subdir, file)
                tempDic = functions.loadBib(pathWhereBibIs)
                publicationDic.update(tempDic)

    # generate data for the main CONTENTS
    singleItemTemplate = '<li><a href="@RELATIVEPATH@/pages/DETAILS.html">[@CITATIONKEY@]</a> @AUTHOROREDITOR@ (@DATE@) - <i>@TITLE@</i></li>'
    contentsList = []

    for citeKey,bibRecord in publicationDic.items():
        relativePath = functions.generatePublPath(pathToMemex, citeKey).replace(pathToMemex, "")

        authorOrEditor = "[No data]"
        if "editor" in bibRecord:
            authorOrEditor = bibRecord["editor"]
        if "author" in bibRecord:
            authorOrEditor = bibRecord["author"]

        date = bibRecord["date"][:4]

        title = bibRecord["title"]

        # forming a record
        recordToAdd = singleItemTemplate
        recordToAdd = recordToAdd.replace("@RELATIVEPATH@", relativePath)
        recordToAdd = recordToAdd.replace("@CITATIONKEY@", citeKey)
        recordToAdd = recordToAdd.replace("@AUTHOROREDITOR@", authorOrEditor)
        recordToAdd = recordToAdd.replace("@DATE@", date)
        recordToAdd = recordToAdd.replace("@TITLE@", title)

        recordToAdd = recordToAdd.replace("{", "").replace("}", "")

        contentsList.append(recordToAdd)

    contents = "\n<ul>\n%s\n</ul>" % "\n".join(sorted(contentsList))
    mainContent = "<h1>CONTENTS of MEMEX</h1>\n\n" + contents

    # save the CONTENTS page
    with open(os.path.join(pathToMemex, "contents.html"), "w", encoding="utf8") as f9:
        f9.write(template.replace("@MAINCONTENT@", mainContent))