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
bibName="testbib.bib"
entries=PDFdl.openBibLib(bibName).entries  #all of the bib's articles
class article:
    def __init__(self, title, author):
        self.title = list 
        self.author = author


def getAll(index,bibName):
    return bibtexparser.customization.convert_to_unicode(entries[index]) 

def getInfo(authorName): #name in the form of lastName
    datesAndIds = dict()
    coauthors=[]
    for i in entries:
        if authorName.replace(" ","") in i["author"].replace(" ","").replace("{","").replace("}",""):
            try:
                datesAndIds[i["title"]]=[i["year"]+" " + i["month"],int(re.findall(regex,i["annote"])[0])] #dictionnary pubName : [date,id]
            except KeyError:
                print "no month available for document"
            for k in i["author"].replace(" ","").replace("{","").replace("}","").split("and"):
                if k not in coauthors:
                    coauthors.append(k.replace('}','').replace('{','').replace(" ",""))        
    coauthors=[i for i in coauthors if i!=authorName]     
    return datesAndIds, coauthors

def getCoauthors(authorName):
    coauthors=[]
    for i in entries:
        if authorName.replace(" ","") in i["author"].replace(" ","").replace("{","").replace("}",""):
            for k in i["author"].replace(" ","").replace("{","").replace("}","").split("and"):
                coauthors.append(k.replace('}','').replace('{','').replace(" ",""))        
    coauthors=[i for i in coauthors if i!=authorName]     
    coauthorsFreq = {a:coauthors.count(a) for a in coauthors}    
    coauthors2=[i for i in coauthorsFreq if coauthorsFreq[i]>10]
    return coauthors2