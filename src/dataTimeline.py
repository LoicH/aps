# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 10:43:42 2016

@author: asueur
"""
from freqMatrixClass import FreqMatrix
from retrieveCategories import getAll
from timelineVisualization import getInfo
#tfid concepts : matrice
# sommer par lignes et normaliser /total
#faire moyennne pour 3 annnees
#convertir au bon format



def createTFIDFMatrix(authorName, startDate, endDate): #date format : year monthNumber
    a = dict() #dictionary of frequency dictionaries for documents
    listTitle=getInfo(authorName)[0] #dictonnary of publications and dates and ids
    titleId=dict()
    for j in listTitle:
        if formatDate(j.values[0])>startDate and formatDate(j.values[0])<endDate:
            titleId[j]=j.values[1]
    for title in titleId: #a modifier pour que ce soit la liste des textes et pas des titres
        fileName=str(titleId[title])+".txt"
        fileText = fileName.read()
        a[title]=(getAll(fileText)[0]) #category frequencies of documents
    fm=FreqMatrix([],[])
    for k in a:
        fm.add_doc(k,a[k])
    return fm.to_TFIDF_Matrix()
