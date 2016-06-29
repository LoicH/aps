# -*- coding: utf-8 -*-
"""
Converts data to JSON files
"""
import json
import numpy as np
import codecs
import os

import variables
###################################################################
#conversion for wordCloud

class Object(object):
    """Used to convert an objet into JSON format"""
    def __init__(self, text=None, size=None):
        self.text = text
        self.size = size
    
def convertDict(dico, file_out):
    """ convert a dictionary to a json file used by the worldcloud
    
        >>> convertDict({"streaming":50,"latency":20}, "static/frequency_list.json")    
    
    @param dico: dictionary you want to convert
    @type dico: dictionary
    
    @param file_out: path you want to save the file to
    @type file_out: string
    
    @return: Nothing
    @rtype: None"""
    string=""
    a = dict()
    L = []
    
    #l1 is the dico but sorted by values
    l1 = sorted([(v,k) for (k,v) in dico.items()], reverse=True)
    for (v,k) in l1:
        a = Object(k,v)
        L.append(json.dumps(a.__dict__))
        string=string+json.dumps(a.__dict__)+","
    string = string[0:-1]
    string=string.replace("text","key").replace("size","value")
    string='{ "tags": ['+string+']}'
    f = open(file_out,'w')
    f.write(string)
    f.close()

    
###################################################################
#conversion for timeLine
    

def convertToMatrice(totalFreqDictList, file_out, timeSections): 
    """ standard input form: [{"a":0.3,"b":0.7},{"a":0.4,"b":0.6}] ordered chronologically
    Used to view the evolution in time of the weights of words
    
    @param totalFreqDictList: list of dictionaries saving the weights of each word 
        at a given time point
    @type totalFreqDictList: list of dictionary {category (string): frequency (float)} 
        ordered chronologically
        example: [{"a":0.3,"b":0.7},{"a":0.4,"b":0.6}] 
                             
    @param file_out: path you want to save the file to
    @type file_out: string
    
    @param timeSections: number of periods chosen
    @type timeSections: int
    
    @return: the TFIDF matrix
    @rtype: TDIDFMatrix """
    categoryDict=dict()
    k=0
    for dic in totalFreqDictList: 
    # search all categories and link each one to an index using a dictionary
        for i in dic.keys():
            if i not in categoryDict:
                    categoryDict[str(k)]=i
                    k+=1
    n = len(categoryDict)
    M=np.zeros((n,timeSections))
    for i in range(n): 
    # creating the matrix (format: python array)
        for j in range(timeSections):
            if categoryDict[str(i)] in totalFreqDictList[j]:
                M[i][j]=totalFreqDictList[j][categoryDict[str(i)]]
    s=""
    M=23*M
    (a,b)=np.shape(M)
    for i in range(a-1): 
    # converting matrix to json format for the timeline
        s2=""
        for j in range(b-1):
            s2+=str(M[i][j])+","
        s2+=str(M[i][b-1])
        s+='{"label":"a","values":'+"["+s2+"]},"
    s2=""
    for j in range(b-1):
        s2+=str(M[a-1][j])
    s+='{"label":"a","values":'+"["+s2+","+str(M[a-1][b-1])
    result = """{"toto":"""+"["+s+"]}]}"
    f=open(file_out,"w") 
    # saving the matrix in json format
    f.write(result) 
    f.close()
    return result
    
    
    ###################################################################
    
#conversion for graph

f=codecs.open(variables.json_dir + os.sep + "departments.json","r","utf-8")
departments=json.load(f)
dptDict=dict() # dictionary linking people and the department they work in 
for department in departments:
    for groups in department["groups"]:
        for person in groups["people"]:
            dptDict[person["name"].title()]=department["name"]+"."+groups["name"]+"."
        



def convertGraph(coauthorDict): 
    """ convert from coauthor dict to input format for graph
    @param coauthorDict: link each author to his coauthor
    @type coauthorDict: dictionary {author (string): list coauthors (list string)}
    

    @return: format for graph coauthor
    @rtype: string {"name":string,"size":int,"imports":string list}, {"name":string,"size":int,"imports":string list}, ... ] """
    
    print "convertGraph is computing the JSON file"    
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
    f= codecs.open(variables.json_dir + os.sep+"readme-flare-imports.json","w","utf-8")
    f.write(jsondata)
    f.close()
    return jsondata
    
def convertGraphTelecom(coauthorDict):
    """ convert from coauthor dict to input format for graph. 
    Only keeps researchers at Telecom Paristech
        
    @param coauthorDict: link each author to his coauthor
    @type coauthorDict: dictionary [author (string): list coauthors (list string)]
    
    @return: format for graph coauthor
    @rtype: [{"name":string,"size":int,"imports":string list}, {"name":string,"size":int,"imports":string list}, ... ] """
    
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
    f= codecs.open(variables.json_dir + os.sep+"readme-flare-imports.json","w","utf-8")
    f.write(jsondata)
    f.close()
    return jsondata
    