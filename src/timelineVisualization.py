# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 11:19:24 2016

@author: asueur
"""

import PDFdl
import latexcodec
import codecs
import re


bib = 'document.bib'  ### bib name (can be modified)
entries=PDFdl.openBibLib(bib).entries #all of the bib's articles

class article:
    def __init__(self, title, author):
        self.title = list 
        self.author = author


def getAll(index):
    return entries[index]

def getInfo(authorLastName):
    dates = dict()
    coauthors=[]
    temp=0
    for i in entries:
        if authorLastName in i["author"]:
            try:
                dates[i["title"]]=i["year"]+" " + i["month"]
            except KeyError:
                print "no month available for document"
                temp+=1
            for k in i["author"].split("and"):
                coauthors.append(k.replace('}','').replace('{',''))
    coauthors=[i for i in coauthors if i!=authorLastName]
    coauthorsFreq=dict()
    for c in coauthors:
        if c in coauthorsFreq:
            coauthorsFreq[c]+=1
        else:
            coauthorsFreq[c]=1
    return dates, coauthorsFreq
        

    