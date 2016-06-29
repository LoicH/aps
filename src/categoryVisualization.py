# -*- coding: utf-8 -*-
"""
Only used for testing purposes
"""
# coding: utf8


def getText(fileName):
    """returns the content of the file in aps/data/
    @return: file data
    @rtype: string"""
    f = open("../data/" + fileName, "r")
    content =f.read()
    f.close()
    return content

import retrieveCategories as ret

def getLinkedWord(category, textList, numberWords = 20): 
    """returns the "numberWords" words linked to a category and with the most occurences
    @param category: The category you want the words linked to
    @type category: string
    
    @param textList: The texts' filename you want to search category in
    @type textList: string list
    
    @param numberWords: number of words you want
    @type numberWords: int
    
    @return: occurences number for each word in this category
    @rtype: int list"""
    wordOcc = dict()      # A MODIFIER: ouvrir fichier dans dossier data
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
    @param word: /
    @type word: string
    
    @param category: one category the word is in 
    @type category: string
    
    @param textList: the list of texts you want to search
    @type textList:  list of string
    
    @param numberTexts: number of top texts you want
    @type numberTexts: int
    
    @return: texts with most occurence (sorted)
    @rtype: string list"""
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
    
