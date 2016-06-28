# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 10:43:42 2016

@author: asueur
"""
from freqMatrixClass import FreqMatrix
from retrieveCategories import getAll
from timelineVisualization import getInfo
from Timeline import formatDate
from TFIDFMatrixClass import TFIDFMatrix
import os
import re
from datetime import date
app_path = os.getcwd().split(os.sep+"aps")[0]+os.sep+"aps"
data = app_path+os.sep+"data"



def createTFIDFMatrix(authorName, startDate, endDate): #date format : year monthNumber
    """ create TFIDF Matrix using documents written by an author during a selected period
    @param authorName : author's lastname
    @type authorName: string
    
    @param startName: start of the period you want to select
    @type startName: string "year monthNumber"
    
    @param endName: end of the period you want to select
    @type endName: string "year monthNumber"
    
    @return: TFIDF Matrix using documents selected
    @rtype: TDIDFMatrix object """
    a = dict() #dictionary of frequency dictionaries for documents
    listTitle=getInfo(authorName)[0] #dictonnary of publications, dates and ids e.g : {pubName : [date,id]}
    titleId=dict()
    for j in listTitle:
        formatedDate=formatDate(listTitle[j][0])
        pubDate=date(int(formatedDate.split()[0]),int(formatedDate.split()[1]),1)
        if pubDate>startDate and pubDate<endDate: #checks if text was published in a fixed time window
            titleId[j]=listTitle[j][1]
    fm=FreqMatrix([],[])
    for title in titleId:
        print titleId[title]
        try:
            fileName=open(data+os.sep+str(titleId[title])+"_out.txt","r") #retrieves the txt of a given publication via its ID
            fileText = fileName.read().replace('\x0c','')
            fileName.close()
            a[title]=getAll(fileText)[0] #category frequencies of documents
        except:
                print "File "+ " not found in directory"
    for k in a:
        fm.add_doc(k,a[k])
    return fm.to_TFIDF_Matrix()

def median(matrixList): 
    """returns average value of category frequencies for multiple TFIDF matrixes
    @param matrixList: TFIDF Matrixes you want average value from
    @type matrixList : list of objects TFIDFMatrix
    
    @return : average value of category frequencies for all categories in those matrices
    @rtype: float list """
    n=len(matrixList) #number of matrixes
    totalFreq=dict()
    dictList=[]  #list of all the total frequency dictionaries from the matrixes
    for m in matrixList:
        m.pretty_print()
        wordDict=m.sum_words()
        dictList.append(wordDict)
    wordList=[] #list of all possible categories/words
    for d in dictList:
        for word in d.keys():
            if word not in wordList:
                wordList.append(word)
    for word in wordList:
        for d in dictList:
            if word in d:
                if word in totalFreq:
                    totalFreq[word]+=d[word]
                else:
                    totalFreq[word]=d[word]
    for i in totalFreq:
        totalFreq[i]=totalFreq[i]/float(n)
    return totalFreq
        

if __name__ == "__main__":
    m1=FreqMatrix([],[])
    m2=FreqMatrix([],[])
    m = FreqMatrix([],[])
    m.add_doc("data science book", {"big data":0.5, "machine learning":0.7, "programming":0.5})
    m1.add_doc("data science book", {"big data":0.5, "machine learning":0.7, "programming":0.5})
    m2.add_doc("data science book", {"big data":0.5, "machine learning":0.7, "programming":0.5})
    m2.add_doc("systems course", {"operating systems":0.8, "programming":0.36})
    m1.add_doc("knuth 101", {"programming":0.45, "operating systems":0.3})
    m.add_doc("knuth 101", {"programming":0.45, "operating systems":0.3})
    m.add_doc("artificial intelligence course", {"programming":0.25,"machine learning":0.5})
    m.add_doc("systems course", {"operating systems":0.8, "programming":0.36})
    tm = m.to_TFIDF_Matrix()
    tm1 = m1.to_TFIDF_Matrix()
    tm2 = m2.to_TFIDF_Matrix()
    
    