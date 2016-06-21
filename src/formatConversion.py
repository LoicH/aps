# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 13:46:30 2016

@author: asueur
"""
import json

class Object(object):
    """__init__() functions as the class constructor"""
    def __init__(self, text=None, size=None):
        self.text = text
        self.size = size


def convertDict(dico):
    string=""
    a= dict()
    L=[]
    for i in dico.keys():
        a=Object(i,dico[i])
        L.append(json.dumps(a.__dict__))
        string=string+json.dumps(a.__dict__)+","
    string = string[0:-1]
    f = open('frequency_list.json','w')
    f.write('{"frequency_list":['+ string+"]}")
    f.close()
    
    