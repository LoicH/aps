# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 18:08:59 2016

@author: asueur
"""

import urllib
import re
import bibtexparser
import os
#constantes
app_path = os.getcwd().split(os.sep+"aps")[0]+os.sep+"aps"
data = app_path+os.sep+"data"
static = app_path+os.sep+"static"
src = app_path+os.sep+"src"
regex=r'id=(\d+)'  

def openBibLib(bibName): # e.g : 'document.bib'
    with open(src+os.sep+bibName) as bibtex_file:  
        bibtex_database = bibtexparser.load(bibtex_file) 
        return bibtex_database

class PDF(object):
    """__init__() functions as the class constructor"""
    def __init__(self, title=None, author=None, id=None, pubDate=None, status=None):
        self.title = title
        self.author = author
        self.id = id
        self.pubDate = pubDate
        

#def download(fileURL,writeFile):
#    testfile = urllib.URLopener()
#    try:
#        testfile.retrieve(fileURL, writeFile)  # example : testfile.retrieve("http://biblio.telecom-paristech.fr/cgi-bin/download.cgi?id=11068", "file.pdf")
#    except IOError:
#        print "No pdf or no memory left"

def downloadPDF(id):
    testfile = urllib.URLopener()
    print  "http://biblio.telecom-paristech.fr/cgi-bin/download.cgi?id="+str(id)
    try:
        if( str(id)+".pdf" in os.listdir(data)): #checks if the file already exists
            print "File already present"

def createPDF(index):
    c=pdfs[index]
    fields=c.split(",") #fields separation
    for i in range(len(fields)):    
        fields[i]=fields[i].split("=")  #values separation
    i=0
    regex2=r'(\d+)'
    pubDate=''
    while i<len(fields):
        if "author" in fields[i][0]:
            author=fields[i][1]
        if "title" in fields[i][0] and not "booktitle" in fields[i][0]:
            title=fields[i][1]
        if "year" in fields[i][0]:
            year=fields[i][1]
            pubDate+=year
        if "month" in fields[i][0]:
            month=fields[i][1]
            pubDate+=month
        if(index>3110):
            print fields[i]
        if "annote" in fields[i][0]:
            temp =re.findall(regex2,fields[i][-1])
            if len(temp)==0:
                return 
            else:
                id=int(temp[0])
        i+=1
    return PDF(title,author,id,pubDate)
    except IOError:
        print "No pdf or no memory left"
        
        
#def downloadPDFfrom(authorName):
#    listTitle=timelineVisualization.getInfo(authorName)[0] #dictonnary of publications, dates and ids e.g : {pubName : [date,id]}
#    print listTitle
#    titleId=dict()
#    for j in listTitle:
#        titleId[j]=listTitle[j][1]
#    for title in titleId:
#        downloadPDF(titleId[title])
    
    
def createPDFList():
    L=[]
    for i in range(1,len(pdfs)):
        print i
        id=int(re.findall(regex,annote)[0])
        downloadPDF(id)
        pos_Id_List[i]=id
        downloadPDF(id)
    return pos_Id_List

