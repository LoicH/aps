# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 14:45:13 2016

@author: asueur
"""
import numpy as np


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
    
