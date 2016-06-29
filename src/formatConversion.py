# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 13:46:30 2016

@author: asueur
"""
import json
import numpy as np
import codecs
import os

###################################################################
#conversion for wordCloud



class Object(object):
    """__init__() functions as the class constructor"""
    def __init__(self, text=None, size=None):
        self.text = text
        self.size = size


def convertDict(dico, file_out):
    """ convert a dictionnary to a json file used by the first worldcloud
    @param dico : dictionnary you want to convert
    @type dico : dictionnary
    
    @param file_out : path you want to save the file to
    @type file_out : string"""
    string=""
    a= dict()
    L=[]
    for i in dico.keys():
        a=Object(i,dico[i])
        L.append(json.dumps(a.__dict__))
        string=string+json.dumps(a.__dict__)+","
    string = string[0:-1]
    f = open(file_out,'w')
    f.write('{"tags":['+ string+"]}")
    f.close()
    
def convertDict2(dico, file_out): #used for the second type of word visualization
    """ convert a dictionnary to a json file used by the second worldcloud
    @param dico : dictionnary you want to convert
    @type dico : dictionnary
    
    @param file_out : path you want to save the file to
    @type file_out : string"""
    string=""
    a= dict()
    L=[]
    l1 = sorted([(v,k) for (k,v) in dico.items()], reverse=True)
    for (v,k) in l1:
        a=Object(k,v)
        L.append(json.dumps(a.__dict__))
        string=string+json.dumps(a.__dict__)+","
    string = string[0:-1]
    string=string.replace("text","key").replace("size","value")
    string='{"tags":'+ "["+string+"]}"
    f = open(file_out,'w')
    f.write(string)
    f.close()

    
###################################################################
#conversion for timeLine
    

def convertToMatrice(totalFreqDictList, file_out, timeSections): 
    """ standard input form : [{"a":0.3,"b":0.7},{"c":0.3,"d":0.7}] ordered chronologically
    @param totalFreqDictList : all category frequencies for all periods previously selected
    @type totalFreqDictList: list of dictionnary[category (string) : frequency (float)] ordered chronologically
                             example : [{"a":0.3,"b":0.7},{"c":0.3,"d":0.7}] 
                             
    @param file_out : path you want to save the file to
    @type file_out : string
    
    @param timeSections : number of periods chosen
    @type timeSections : int
    
    @return: Matrix used by the timeline (ligns : categories, columns : timeSections, coef : category weight in this timeSection)
    @rtype: TDIDFMatrix object """
    categoryDict=dict()
    k=0
    for dic in totalFreqDictList: # search all categories and link each one to an index using a dictionnary
        categories=dic.keys()
        for i in categories:
            if i not in categoryDict:
                    categoryDict[str(k)]=i
                    k+=1
    n = len(categoryDict)
    M=np.zeros((n,timeSections))
    for i in range(n): # creating the matrix (format : python array)
        for j in range(timeSections):
            if categoryDict[str(i)] in totalFreqDictList[j]:
                M[i][j]=totalFreqDictList[j][categoryDict[str(i)]]
    s=""
    M=23*M
    (a,b)=np.shape(M)
    
    listNormalValues=[]
    for j in range(b):
        normalValue=0
        for i in range(a):
            normalValue+=M[i][j]
        listNormalValues.append(23*normalValue)
    for i in range(a-1): # converting matrix to json format for the timeline
        s2=""
        for j in range(b-1):
            s2+=str(M[i][j]/listNormalValues[j])+","
        s2+=str(M[i][b-1]/listNormalValues[b-1])
        s+='{"label":"'+categoryDict[str(i)]+'","values":'+"["+s2+"]},"
    s2=""
    for j in range(b-1):
        s2+=str(M[a-1][j]/listNormalValues[j])
    s+='{"label":"'+categoryDict[str(a-1)]+'","values":'+"["+s2+","+str(M[a-1][b-1]/listNormalValues[b-1])
    result = """{"toto":"""+"["+s+"]}]}"
    f=open(file_out,"w") # saving the matrix in json format
    f.write(result) 
    f.close()
    return result
    
    
    ###################################################################
    
#conversion for graph

f=codecs.open("departments.json","r","utf-8") #json of departments
departments=json.load(f)
dptDict=dict() # dictionary linking people and the department they work in 
for department in departments:
    for groups in department["groups"]:
        for person in groups["people"]:
            dptDict[person["name"].title()]=department["name"]+"."+groups["name"]+"."
        



def convertGraph(coauthorDict): 
    """ convert from coauthor dict to input format for graph
    @param coauthorDict: link each author to his coauthor
    @type coauthorDict: dictionnary [author (string): list coauthors (list string)]
    

    @return : format for graph coauthor
    @rtype : [{"name":string,"size":int,"imports":string list}, {"name":string,"size":int,"imports":string list}, ... ] """
    
    jsondata="["
    for i in coauthorDict:
        dpt=""
        try:
            name=i.split(".")[1].replace(" ","")
            if name in dptDict.keys():
                dpt=dptDict[name]
        except:
            print "non regular name"
        jsondata+="""{"name":"""+'"'+dpt+i.replace(".","")+'"'+""","size":3000,"imports":["""
        for k in coauthorDict[i]:
            dpt=""
            try:
                name=k.split(".")[1].replace(" ","")
                if name in dptDict.keys():
                    dpt=dptDict[name]
            except:
                print "non regular name"

            jsondata+='"'+dpt+k.replace(".","")+'"'+","
        if jsondata[-1]!="[":
            jsondata=jsondata[:-1]
        jsondata=jsondata+"]},"
    jsondata=jsondata[:-1]
    jsondata+="]"
    f= codecs.open("templates" + os.sep+"readme-flare-imports.json","w","utf-8")
    f.write(jsondata)
    f.close()
    return jsondata
    
def convertGraphTelecom(coauthorDict):
    """ convert from coauthor dict to input format for graph // only keeps researchers at Telecom Paristech
    @param coauthorDict : link each author to his coauthor
    @type coauthorDict : dictionnary [author (string) : list coauthors (list string)]
    
    @return : format for graph coauthor
    @rtype : [{"name":string,"size":int,"imports":string list}, {"name":string,"size":int,"imports":string list}, ... ] """
    
    jsondata="["
    for author, coauthors in coauthorDict.items():
        dpt=""
        try:
            name=author.split(".")[1].replace(" ","")
            if name in dptDict.keys():
                dpt=dptDict[name]
                jsondata+="""{"name":"""+'"'+dpt+author.replace(".","")+'"'+""","size":3000,"imports":["""
                for coauthor in coauthors:
                    dpt=""
                    try:
                        name=coauthor.split(".")[1].replace(" ","")
                        if name in dptDict.keys():
                            dpt=dptDict[name]
                            jsondata+='"'+dpt+coauthor.replace(".","")+'"'+","
                    except:
                        print "non regular name"  
                if jsondata[-1]!="[":
                    jsondata=jsondata[:-1]
                jsondata=jsondata+"]},"
        except:
            print "non regular name"  
                
        
    jsondata=jsondata[:-1]
    jsondata+="]"
    f= codecs.open("templates" + os.sep+"readme-flare-imports.json","w","utf-8")
    f.write(jsondata)
    f.close()
    return jsondata
    