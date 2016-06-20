# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 16:42:50 2016

@author: asueur
"""





# blackList : banned words list
import string
from nltk import *
import os

#tests
pdfPath = "/cal/homes/asueur/Downloads/TP3.pdf"
text1 = "abc Abc bAc.... bBc bacb acb acb acb and ant ham"
randomText="Still court no small think death so an wrote. Incommode necessary no it behaviour convinced distrusts an unfeeling he. Could death since do we hoped is in. Exquisite no my attention extensive. The determine conveying moonlight age. Avoid for see marry sorry child. Sitting so totally forbade hundred to.Their could can widen ten she any. As so we smart those money in. Am wrote up whole so tears sense oh. Absolute required of reserved in offering no. How sense found our those gay again taken the. Had mrs outweigh desirous sex overcame. Improved property reserved disposal do offering me"
blackList=["abc","acb"]


#deleting punctuation
def delPunctuation(text):
    for char in string.punctuation: 
        text=text.replace(char,'')
    return text
    
def getTextWords(text):
    return word_tokenize(text)

#deleting useless words + lowercase
def modifyText(textWords, blackList):
    for i in range(len(textWords)):
        if(textWords[i].islower()):
            textWords[i]=textWords[i].lower()
    for i in blackList :
        textWords = textWords.replace(i,'')
    return textWords
    
    
    
    

    
def deleteStopWords(textWords):
    #deleting words of types determiners, conjonctions, cardinal numbers and stopwords
    listCopy=textWords
    stopwords= corpus.stopwords.words("english")
    for sw in stopwords:
        listCopy=[j for j in listCopy if j!=str(sw)]
    types = nltk.pos_tag(listCopy)      
    for i in types:
        if i[1] in ["DT","CC", "CD", "PRP", "PRP$", "PDT"] :  
            listCopy.remove(i[0])
    return listCopy
    
def lemmatization(textWords):
    words = textWords
    lmtzr=WordNetLemmatizer()
    for i in range(len(words)):
        words[i]=str(lmtzr.lemmatize(words[i]))
    return words
    
    
#def compteur(text, wordList):
#    text=delPunctuation(text)
#    dictionnary={}
#    textWords=text.split()
#    for word in wordList:
#        a=0
#        for word2 in textWords:
#            if (word==word2):
#                a+=1
#            dictionnary[word]=str(a/float(len(textWords)))
#    return dictionnary
    
        
def frequency(textWords):
    a=FreqDist(textWords)
    length=len(a)
    for i in a.keys():
        a[i]=a[i]/float(length)
    return a