# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 18:28:52 2016

@author: loic

Class defining matrix behavior
"""

class TFIDFMatrix():
    """Contains a graph linking documents and words"""
    def __init__(self, docs_list, words_list):
        self.words = words_list #words list to link words to index
        self.graph = dict()
        for doc in docs_list:
            self.graph[doc] = dict()
        
    def coef(self, doc, word):
        """returns the TFIDF value linking doc and word"""
        try:
            return self.graph[doc][word]
        except:
            return 0
    
    def word_appearance(self,word):
        appearance = dict()
        for doc, dictionary in self.graph:
            try:
                appearance[doc] = dictionary[word]
            except:
                appearance[doc] = 0
        return appearance
        
