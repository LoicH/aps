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
src = app_path+os.sep+"src"
regex=r'id=(\d+)'  

def openBibLib(bibName): # e.g : 'document.bib'
    with open('document.bib') as bibtex_file:  
        bibtex_database = bibtexparser.load(bibtex_file) 
        return bibtex_database


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
        else:
            print id
            testfile.retrieve("http://biblio.telecom-paristech.fr/cgi-bin/download.cgi?id="+str(id), "/tmp"+os.sep+str(id)+".pdf")
    except IOError:
        print "No pdf or no memory left"
        
def downloadAll(bibName): #downloads all files from a given bibTex library
    pos_Id_List = dict()
    bibtex_database=openBibLib(bibName)
    for i in range(len(bibtex_database.entries)):
        try:
            annote=bibtex_database.entries[i]["annote"]
        except KeyError:
            print "No id found"
        print i
        id=int(re.findall(regex,annote)[0])
        pos_Id_List[i]=id
        downloadPDF(id)
    return pos_Id_List

