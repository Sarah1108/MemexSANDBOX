#### wordcloud
#### import libraries
import yaml
import functions
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
import json
###########################################################
#####load settings file############
settingsFile = "settings.yml"
settings = yaml.safe_load(open(settingsFile))
#####load memexPath ##############
memexPath = settings["path_to_memex"]

##### 

#ocrFiles = functions.dicOfRelevantFiles(memexPath, ".json")   
#citeKeys = list(ocrFiles.keys())
#savePath =  os.path.join(memexPath,"wordcloud" + ".jpg")

#print(tfidfDic)
def createWordCloud(savePath, tfIdfDic):
    wc = WordCloud(width=1000, height=600, background_color="white", random_state=2,
                   relative_scaling=0.5, colormap="gray") 
    wc.generate_from_frequencies(tfIdfDic)
    # plotting
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    #plt.show() # this line will show the plot
    plt.savefig(savePath, dpi=200, bbox_inches='tight')


def processAllclouds(filename):

    docData = json.load(open(filename, "r", encoding="utf8")) ## loads tfidf file 

    for k, v in docData.items(): ###loop through the file
        savePath = functions.generatePublPath(memexPath, k) ##create path for file
        savePath = savePath + "\\" + k
        if v:
            createWordCloud(savePath, v) ### create wordcloud
processAllclouds("tfidfTableDic_filtered.txt")
