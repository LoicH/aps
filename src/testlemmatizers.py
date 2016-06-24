# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 10:56:34 2016

@author: alagasse
"""

#ADJ, ADJ_SAT, ADV, NOUN, VERB = 'a', 's', 'r', 'n', 'v'

import modifTexte
from nltk import *


def wLemmatization(textWords): # test lemmatization with wordnet
    return modifTexte.lemmatization(textWords)

def sStemmatization(textWords): #test stemmatization with snowballstemmer
    #lemmatizes all the words
    words = textWords
    snowball_stemmer = SnowballStemmer("english")
    for i in range(len(words)):
        words[i]=snowball_stemmer.stem(words[i])
    return words

def textToDictionnary(text, blackList):
    return wLemmatization(deleteStopWords(modifyText(getTextWords(delPunctuation(text)),blackList)))

    
def get_wordnet_pos(treebank_tag): # convert pos_tag from nltk to pos_tag from wordnet

    if treebank_tag.startswith('J'):
        return "a"
    elif treebank_tag.startswith('V'):
        return "v"
    elif treebank_tag.startswith('N'):
        return "n"
    elif treebank_tag.startswith('R'):
        return "r"
    else:
        return 'n'
        
#comparison wordnet with and without taking account of post_tag
lmtzr=WordNetLemmatizer()

#text used as test
text = word_tokenize("""The aim of a probabilistic logic (also probability logic and probabilistic reasoning) is to combine the capacity of probability theory to handle uncertainty with the capacity of deductive logic to exploit structure of formal argument. The result is a richer and more expressive formalism with a broad range of possible application areas. Probabilistic logics attempt to find a natural extension of traditional logic truth tables: the results they define are derived through probabilistic expressions instead. A difficulty with probabilistic logics is that they tend to multiply the computational complexities of their probabilistic and logical components. Other difficulties include the possibility of counter-intuitive results, such as those of Dempster-Shafer theory. The need to deal with a broad variety of contexts and issues has led to many different proposals.""")
p = pos_tag(text)

#print words that are different with and without taking account of post_tag
for i in p :
    if(lmtzr.lemmatize(i[0]) != lmtzr.lemmatize(i[0], get_wordnet_pos(i[1])))  :
        print("Original word in text: " + i[0])
        print("Basic Lemmatization : " + lmtzr.lemmatize(i[0]))
        print("Smart Lemmatization : " + lmtzr.lemmatize(i[0], get_wordnet_pos(i[1])))
        print("")
    

