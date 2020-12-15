###Pseudocode index
# load page template
#import libraries
import os, json
import functions 
import yaml


### variables
settingsFile = "./settings.yml"
settings = yaml.safe_load(open(settingsFile))
memexPath = settings["path_to_memex"]

#load template_index
with open(settings["template_index"], "r", encoding="utf8") as ft:
    template = ft.read()