# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 13:46:30 2016

@author: asueur
"""
import json
import numpy as np


###################################################################
#conversion for wordCloud

class Object(object):
    """__init__() functions as the class constructor"""
    def __init__(self, text=None, size=None):
        self.text = text
        self.size = size


def convertDict(dico, file_out):
    string=""
    a= dict()
    L=[]
    for i in dico.keys():
        a=Object(i,dico[i])
        L.append(json.dumps(a.__dict__))
        string=string+json.dumps(a.__dict__)+","
    string = string[0:-1]
    f = open(file_out,'w')
    f.write('{"frequency_list":['+ string+"]}")
    f.close()
    
###################################################################
#conversion for timeLine
    
timeSections=10 #number of time sections considered

def convertToMatrice(totalFreqDictList): # standard input form : [{"a":0.3,"b":0,7},{"c":0.3,"d":0,7}] ordered chronologically
    categoryDict=[]
    k=0
    for dic in totalFreqDictList:
        categories=dic.keys()
        for i in categories:
            if i not in categoryDict:
                    categoryDict[str(k)]=i
                    k+=1
    n = len(categoryDict)
    M=np.zeroes((n,timeSections))
    for i in range(n):
        for j in range(timeSections):
            if categoryDict[i] in totalFreqDictList[j]:
                M[i][j]=totalFreqDictList[j][categoryDict[i]]
    return M
    