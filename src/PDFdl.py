# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 18:08:59 2016

@author: asueur
"""

import urllib
import re

# regex=r'id=(\d+)}'  



class PDF(object):
    """__init__() functions as the class constructor"""
    def __init__(self, title=None, author=None, id=None, pubDate=None, status=None):
        self.title = title
        self.author = author
        self.id = id
        self.pubDate = pubDate
        

def download(fileURL,writeFile):
    testfile = urllib.URLopener()
    testfile.retrieve(fileURL, writeFile)  # example : testfile.retrieve("http://biblio.telecom-paristech.fr/cgi-bin/download.cgi?id=11068", "file.pdf")



if __name__ == "__main__":
    f = open("document.bib", "r")
    lines = f.readlines()
    s = ''                   #str = text of the file document.bib
    for i in range(len(lines)):
        s += lines[i].rstrip('\n') + ' '
    
    
    pdfs=re.split(r'@[article|inproceedings|workshop|invite|incollection|grandpublic|proceedings|multimedia|book|inbook|booklet|manual|phdthesis|mastersthesis|rapcontrat|raprech|raphdr|techreport|reference|standardisation|brevet|unpublished|misc]+',s)

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
    
    
def createPDFList():
    L=[]
    for i in range(1,len(pdfs)):
        print i
        pdf=createPDF(i)
        if pdf is not None:
            L.append(pdf)
            print(pdf.title)
    return L