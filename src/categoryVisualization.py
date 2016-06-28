# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 10:33:11 2016

@author: asueur
"""
# coding: utf8


def getText(fileName) :
    """returns the content of the file in aps/data/"""
    f = open("../data/" + fileName, "r")
    content =f.read()
    f.close()
    return content

import retrieveCategories as ret
#trouver mots liés concept dans dictionnaire de chacun des documents / concaténer
#garder mot avec plus grande fréquence
# quand on clique sur un mot : parcourir l'ensemble des mots liés à ce concept dans chaque document et compter nombre occurences

def getLinkedWord(category, textList, numberWords = 20): 
    """returns the "numberWords" words linked to a category and with the most occurences
    @param category: The category you want the words linked to
    @type category: ???
    
    @param textList: ???
    @type textList: ???
    
    @param numberWords: number of words you want
    @type numberWords: int"""
    wordOcc = dict()      # A MODIFIER : ouvrir fichier dans dossier data
    for text in textList:
        file = open(text, "r")
        content = file.read()
        URIs= ret.getURIs(content)
        categories=ret.getCategories(URIs[0],URIs[1])[1]
        for word in categories[category]:
            if word in wordOcc:
                wordOcc[word]+=1
            else:
                wordOcc[word]=1
        file.close()
    sortedOcc= sorted([(k) for (k,v) in wordOcc.items()],reverse=True)[:numberWords]
    return sortedOcc
    
def getTextWithMostOccurenceOf(word, category, textList, numberTexts = 1): 
    """gets list of texts with the highest frequency of the word
    @param word:
    @type word:
    
    @param category:
    @type category:
    
    @param textList: the list of texts you want to search
    @type textList:  list of <str/unicode ??>
    
    @param numberTexts: number of top texts you want
    @type numberTexts: int"""
    occWordByText= dict()
    for text in textList:
        i=0
        URIs= ret.getURIs(text)
        categories=ret.getCategories(URIs[0],URIs[1])[1]
        for w in categories[category]:
            if w==word:
                i+=1
        occWordByText[text]=float(i)/len(text.split())
    sortedText= sorted([(k) for (k,v) in occWordByText.items()],reverse=True)[:numberTexts]
    return sortedText
    