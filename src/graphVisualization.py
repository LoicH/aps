# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 11:36:10 2016

@author: asueur
"""

import PDFdl
import dateTimeline
import numpy as np



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
        authors=article["author"].replace("{","").replace("}","").split("and")
        for author in authors:
            if author not in authorList:
                authorList.append(author)
    return authorList
    
def getdictCoauthors(authorList):
    dictCoauthors=dict()
    for author in authorList:
        