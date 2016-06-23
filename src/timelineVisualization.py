# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 11:19:24 2016

@author: asueur
"""

import PDFdl
import bibtexparser


bib = 'document.bib'  ### bib name (can be modified)
entries=PDFdl.openBibLib(bib).entries #all of the bib's articles

class article:
    def __init__(self, title, author):
        self.title = list 
        self.author = author


def getAll(index):
    return bibtexparser.customization.convert_to_unicode(entries[index]) 

def getInfo(authorName): #name in the form of Initial. lastName
    dates = dict()
    coauthors=[]
    temp=0
    for i in entries:
        if authorName in i["author"]:
            try:
                dates[i["title"]]=i["year"]+" " + i["month"]
            except KeyError:
                print "no month available for document"
                temp+=1
            for k in i["author"].split("and"):
                coauthors.append(k.replace('}','').replace('{','').replace(" ",""))
                
    coauthors=[i for i in coauthors if i!=authorName]
    
    coauthorsFreq = {a:coauthors.count(a) for a in coauthors}    
    
    return dates, coauthorsFreq
        

    