# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 17:31:07 2016

@author: asueur
"""
import numpy as np

def sumTFIDF(matrix,dict1):
    dico=dict()
    m=np.shape(matrix)[1]
    for word in dict1:
        sum=0
        for j in range(m):
            sum=sum+matrix[dict1[word]][j]
        dico[word]=sum*50
    return dico