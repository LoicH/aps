# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 14:45:13 2016

@author: asueur
"""
import numpy as np
#scalar product between
#def normalizedScalarProduct(matrice, numTextDic, text1, text2):
#    scal=0
#    i=numTextDic[text1]
#    j=numTextDic[text2]
#    scal=np.dot(matrice[:,i],matrice[:,j])/float(np.linalg.norm(x)*np.linalg.norm(y))
#    return scal
    

#similarity matrix 
def similarityMatrix(matrice):
    similarity = np.dot(matrice, matrice.T)
    square_mag = np.diag(similarity)
    inv_square_mag = 1.0 / square_mag
    inv_square_mag[np.isinf(inv_square_mag)] = 0
    inv_mag = np.sqrt(inv_square_mag)
    cosine = similarity * inv_mag
    cosine = cosine.T * inv_mag
    return cosine
    
