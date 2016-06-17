# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 16:42:50 2016

@author: asueur
"""


#text : texte extrait après conversion depuis pdf
# listeCreux : list des mots creux

import string
from nltk import *
import os
pdfPath = "/cal/homes/asueur/Downloads/TP3.pdf"
text = "abc Abc bAc.... bBc bacb acb acb acb and ant ham"
randomText="Still court no small think death so an wrote. Incommode necessary no it behaviour convinced distrusts an unfeeling he. Could death since do we hoped is in. Exquisite no my attention extensive. The determine conveying moonlight age. Avoid for see marry sorry child. Sitting so totally forbade hundred to.Their could can widen ten she any. As so we smart those money in. Am wrote up whole so tears sense oh. Absolute required of reserved in offering no. How sense found our those gay again taken the. Had mrs outweigh desirous sex overcame. Improved property reserved disposal do offering me"
blackList=["abc","acb"]

def delPunctuation(text):
    for char in string.punctuation: 
        text=text.replace(char,'')
    return text

#suppression mots creux + mise en minuscules minuscules
def modifyText(text, blackList):
    text=text.lower()
    for i in blackList :
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
        
def frequency(text):
    a=FreqDist(nltk.word_tokenize(text))
    length=len(a)
    for i in a.keys():
        a[i]=a[i]/float(length)
    return a
    
def deleteStopWords(text):
    #suppression de déterminants, conjonctions, nombres
    listCopy=word_tokenize(delPunctuation(text))
    types = nltk.pos_tag(listCopy)
    for i in types:
        if i[1] in ["DT","CC", "CD", "PRP", "PRP$", "PDT"] :  
            listCopy.remove(i[0])
    return listCopy
    
def lemmatization(text):
    words = nltk.word_tokenize(text)
    lmtzr=WordNetLemmatizer()
    for i in range(len(words)):
        words[i]=str(lmtzr.lemmatize(words[i]))
    return words