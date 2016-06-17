# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 16:42:50 2016

@author: asueur
"""


#text : texte extrait après conversion depuis pdf
# listeCreux : list des mots creux

import string
from  nltk import *
import os
pdfPath = "/cal/homes/asueur/Downloads/TP3.pdf"
text = "abc Abc bAc.... bBc bacb acb acb acb"
listeCreux=["abc","acb"]

def delPunctuation(text):
    for char in string.punctuation: 
        text=text.replace(char,'')
    return text

#suppression mots creux + mise en minuscules minuscules
def modifyText(text, listeCreux):
    text=text.lower()
    for i in listeCreux :
        text = text.replace(i,'')
    return text
    
    
    
    
def compteur(text, wordList):
    text=delPunctuation(text)
    dictionnary={}
    textWords=text.split()
    for word in wordList:
        a=0
        for word2 in textWords:
            if (word==word2):
                a+=1
            dictionnary[word]=str(a/float(len(textWords)))
    return dictionnary
        
def convertToText(textPath):
    os.system("pdftotext '%s' '%s'" % (pdfPath, "TP3.txt"))