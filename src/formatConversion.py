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
    
def convertDict2(dico, file_out): #used for the second type of word visualization
    string=""
    a= dict()
    L=[]
    for i in dico.keys():
        a=Object(i,dico[i])
        L.append(json.dumps(a.__dict__))
        string=string+json.dumps(a.__dict__)+","
    string = string[0:-1]
    string=string.replace("text","key").replace("size","value")
    string='{ "tags" : ['+string+']}'
    f = open(file_out,'w')
    f.write(string)
    f.close()

    
###################################################################
#conversion for timeLine
    

def convertToMatrice(totalFreqDictList, file_out, timeSections): 
# standard input form : [{"a":0.3,"b":0.7},{"c":0.3,"d":0.7}] ordered chronologically
    categoryDict=dict()
    k=0
    for dic in totalFreqDictList:
        categories=dic.keys()
        for i in categories:
            if i not in categoryDict:
                    categoryDict[str(k)]=i
                    k+=1
    n = len(categoryDict)
    M=np.zeros((n,timeSections))
    for i in range(n):
        for j in range(timeSections):
            if categoryDict[str(i)] in totalFreqDictList[j]:
                M[i][j]=totalFreqDictList[j][categoryDict[str(i)]]
    s=""
    M=23*M
    (a,b)=np.shape(M)
    for i in range(a-1):
        s2=""
        for j in range(b-1):
            s2+=str(M[i][j])+","
        s2+=str(M[i][b-1])
        s+="["+s2+"],"
    s2=""
    for j in range(b-1):
        s2+=str(M[a-1][j])
        print(s2)
    s+="["+s2+","+str(M[a-1][b-1])
    result = """{"data":"""+"["+s+"]]}"
    f=open(file_out,"w")
    f.write(result)
    f.close()
    return result
    
    
    ###################################################################
#conversion for graph


def convertGraph(coauthorDict): #convert from coauthor dict to input format for graph
    s=""
    for i in coauthorDict:
        s+="""{"name":"""+i+""""size":3000,"imports":"""+str(coauthorDict[i])+"},"
    s=s[:-1]
    return "["+s+"]"
    