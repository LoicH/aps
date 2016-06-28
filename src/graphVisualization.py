# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 11:36:10 2016

@author: asueur
"""

import PDFdl
import numpy as np
import timelineVisualization
import TFIDFMatrixClass


#similarity matrix 
def similarityMatrix(matrice):
    similarity = np.dot(matrice, matrice.T)
    square_mag = np.diag(similarity)
    inv_square_mag = 1.0 / square_mag
    inv_square_mag[np.isinf(inv_square_mag)] = 0
    inv_mag = np.sqrt(inv_square_mag)
    cosine = similarity * inv_mag
    cosine = cosine.T * inv_mag
    return cosine
    
def distanceTFIDF(A,B):
    A.sum_words()
    B.sum_words()
    return 

def getAllAuthors(bibName): #renvoie la liste de tous les auteurs
    authorList=[]
    bibli = PDFdl.openBibLib(bibName)
    for article in bibli.entries:
        authors=article["author"].replace("{","").replace("}","").replace(" ","").split("and")
        for author in authors:
            if author not in authorList:
                authorList.append(author)
    return authorList
    
def getdictCoauthors(bibName):
    authorList=getAllAuthors(bibName)
    n=len(authorList)
    dictCoauthors=dict()
    i=0
    for author in authorList:
        if author!='':
            dictCoauthors[unicode(author)]=timelineVisualization.getCoauthors(author)
        i+=1
        if i%100==0:
            print str(100*float(i)/n) + "% completed"
    return dictCoauthors
    
