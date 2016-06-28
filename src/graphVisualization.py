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
def similarityMatrix(matrix):
    """ tell if documents in a matrix are close or not"""
    similarity = np.dot(matrix, matrix.T)
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

def getAllAuthors(bibName): 
    """ return a list with all the authors in the bib
    @param bibName: the bib you want to get the authors from
    @type bibName: string
                             
    @return: all authors from the bib
    @rtype: string list """
    authorList=[]
    bibli = PDFdl.openBibLib(bibName)
    for article in bibli.entries:
        authors=article["author"].replace("{","").replace("}","").split(" and ")
        for author in authors:
            if author not in authorList:
                authorList.append(author)
    return authorList
    
def getdictCoauthors(bibName):
    """ return a list with all the coauthors in the bib
    @param bibName: the bib you want to get the coauthors from
    @type bibName: string
                             
    @return: all coauthors from the bib linked to the authors
    @rtype: dictionnary[author (string): list coauthors (string list)] """
    authorList=getAllAuthors(bibName)
    n=len(authorList)
    dictCoauthors=dict()
    i=0
    for author in authorList:
        if author!='':
            coauthors=timelineVisualization.getCoauthors(author)
            if coauthors!=[]:
                dictCoauthors[unicode(author)]=coauthors
        i+=1
        if i%100==0:
            print str(100*float(i)/n) + "% completed"
    for i in dictCoauthors.values():
        for k in i:
            if k not in dictCoauthors.keys():
                dictCoauthors[k]=[]
    return dictCoauthors
    
