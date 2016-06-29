# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 11:36:10 2016

@author: asueur
"""

import PDFdl
import numpy as np
import timelineVisualization
import TFIDFMatrixClass
import dataTimeline
from datetime import date


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
    """ return a number related to the similarity between matrixes
    @param A,B : TFIDF matrixes to compare
    @type bibName : TFIDFMatrix
                             
    @return: similarity coefficient
    @rtype: float  
    """
    a=A.sum_words()
    b=B.sum_words()
    for word in b:
        if word not in a:
            a[word]=0
    for word in a:
        if word not in b:
            b[word]=0
    scal=0
    for i in a:
        scal+=a[i]*b[i]
    return scal
    
def getPredictedAuthors(bibName):
    
        predictedDict=dict()
        TFIDFdict=dict()
        authorList=getAllAuthors(bibName)
        for authorName in authorList:
            predictedDict[authorName]=dict()
            TFIDFdict[authorName]=dataTimeline.createTFIDFMatrix(authorName, date(2015,1,1),date(2016,1,1)) #similarity on recent years
        n= len (authorList)
        for i in range(n):
            for j in range(n):
                if j<i:
                    name1=authorList[i]
                    name2=authorList[j]
                    d=distanceTFIDF(TFIDFdict[name1],TFIDFdict[name2])
                    predictedDict[name1][name2]=d
                    predictedDict[name2][name1]=d
                else:
                    break
        finalDict=dict()
        for authorName in authorList:
            values_sorted = sorted([(v,k) for (k,v) in predictedDict[authorName].items()], reverse=True)[:3]
            finalDict[authorName] = [k for (v,k) in values_sorted]
        return finalDict
       

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
    
def getdictCoauthors(bibName, minFreq):
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
            coauthors=timelineVisualization.getCoauthors(author, minFreq)
            if coauthors!=[]:
                dictCoauthors[unicode(author)]=coauthors
        i+=1
        if i%100==0:
            print str(int(100*float(i)/n)) + "% completed"
    for i in dictCoauthors.values():
        for k in i:
            if k not in dictCoauthors.keys():
                dictCoauthors[k]=[]
    return dictCoauthors
    
