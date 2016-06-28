# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 11:36:10 2016

@author: asueur
"""

import PDFdl
import numpy as np
import timelineVisualization



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
    

def getAllAuthors(bibName): #renvoie la liste de tous les auteurs
    authorList=[]
    bib = PDFdl.openBibLib(bibName)
    for article in bib.entries:
        authors=article["author"].replace("{","").replace("}","").replace(" ","").split("and")
        for author in authors:
            if author not in authorList:
                authorList.append(str(author))
    return authorList
    
def getdictCoauthors(bibName):
    authorList=getAllAuthors(bibName)
    dictCoauthors=dict()
    i=0
    for author in authorList:
        dictCoauthors[str(author)]=timelineVisualization.getInfo(author)[1]
        if i==3:
            break
        i+=1
    return dictCoauthors
    


