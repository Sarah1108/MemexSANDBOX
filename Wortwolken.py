#### wordcloud
#### import libraries
import yaml
import functions
from wordcloud import WordCloud
import matplotlib.pyplot as plt
###########################################################
#####load settings file############
settingsFile = "settings.yml"
settings = yaml.safe_load(open(settingsFile))
#####load memexPath ##############
memexPath = settings["path_to_memex"]

##### 

#def processAllFiles(pathToMemex):


    #savepath = dictionaryofRelevantFiles(memexPath, ".jpg")
    #tfIdfDic = 
    #allData = createWordCloud(savePath, tfIdfDic) #loads the bib file
    
    #for k,v in bibData.items():        
    #    language = checkLangId(v)

    #ocrPublication(pathToMemex, k, language)

#processAllFiles(memexPath)

alexanderShouldLiberalArts2012 = {
    "alexander": 0.06937423479907452,
    "campus": 0.19722438810247864,
    "campuses": 0.23136957904341637,
    "centers": 0.1591423737006339,
    "collaboration": 0.08317950971803874,
    "collaborative": 0.056639001811766586,
    "college": 0.19419086335462832,
    "colleges": 0.380461997900762, 
    "davis": 0.11568478952170819,
    "expertise": 0.06337966673661696,
    "faculty": 0.1294605755697522,
    "frost": 0.10706103732461046,
    "grant": 0.0868072776983855,
    "grants": 0.05430051358860444,
    "hamilton": 0.0807076748581175,
    "institutions": 0.08714043875223106,
    "isolation": 0.05041366293632852,
    "liberal": 0.6177958395339113,
    "neh": 0.07183028896816589,
    "pedagogical": 0.061904349203346046,
    "program": 0.057871518465590334,
    "rebecca": 0.10283092401929617,
    "sector": 0.06291941864457654,
    "thatcamp": 0.05869649080590363,
    "undergraduate": 0.19656033193071115,
    "undergraduates": 0.06603355215664158,
    "universities": 0.056639001811766586
    }

savePath = memexPath+".jpg"


def createWordCloud(savePath, tfIdfDic):
    wc = WordCloud(width=1000, height=600, background_color="white", random_state=2,
                   relative_scaling=0.5, colormap="gray") 
    wc.generate_from_frequencies(tfIdfDic)
    # plotting
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    #plt.show() # this line will show the plot
    plt.savefig(savePath, dpi=200, bbox_inches='tight')

createWordCloud(savePath, alexanderShouldLiberalArts2012)