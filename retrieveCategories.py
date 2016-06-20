# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 16:24:43 2016

@author: asueur
"""

import spotlight



def getURIs(text):
    L=[]
    annotations = spotlight.annotate('http://spotlight.sztaki.hu:2222/rest/annotate',text,confidence=0.4, support=20, spotter='Default')
    for i in annotations:
        L.append[i["URI"]]
        print i["URI"]
                           