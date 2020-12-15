### Übertrage die citationkeys in ein yaml
language: 
#function pas as argument lang value i grab from the bib record: 
#is this value empty? -> no language, so go with the language that is most common in my bibliography so maybe eng
#is a language there? Match in the dicitionary with language
#have a language but it's not in the dictonary-> print the language and stop the code (add it manually to the yaml file)
# impose a particular language (if you have some information use it!)

def languageKey():
    if key == "language":
        if ";" in val:
        #print(val)
        temp = val.split(";")

        for t in temp:
            if t.endswith(".pdf"):
            val = t