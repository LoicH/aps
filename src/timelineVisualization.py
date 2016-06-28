# -*- coding: utf-8 -*-

import PDFdl
import bibtexparser
import re
import os

app_path = os.getcwd().split(os.sep+"aps")[0]+os.sep+"aps"
data = app_path+os.sep+"data"
src = app_path+os.sep+"src"

regex=r'id=(\d+)' 
bib = data+os.sep+'document.bib'  ### bib name (can be modified)
entries=PDFdl.openBibLib(bib).entries #all of the bib's articles

class article:
    def __init__(self, title, author):
        self.title = list 
        self.author = author


def getAll(index):
    return bibtexparser.customization.convert_to_unicode(entries[index]) 

def getInfo(authorName): #name in the form of lastName
    datesAndIds = dict()
    coauthors=[]
    temp=0
    for i in entries:
        if authorName.replace(" ","") in i["author"].replace(" ","").replace("{","").replace("}",""):
            try:
                datesAndIds[i["title"]]=[i["year"]+" " + i["month"],int(re.findall(regex,i["annote"])[0])] #dictionnary pubName : [date,id]
            except KeyError:
                print "no month available for document"
                temp+=1
            for k in i["author"].replace(" ","").replace("{","").replace("}","").split("and"):
                if k not in coauthors:
                    coauthors.append(k.replace('}','').replace('{','').replace(" ",""))        
    coauthors=[i for i in coauthors if i!=authorName]     
    return datesAndIds, coauthors

if __name__ == "__main__": 
    print "main"