# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 18:28:52 2016

@author: loic

Class defining matrix behavior
"""

from math import log

from TFIDFMatrixClass import *

class FreqMatrix:
    """Contains a graph linking documents and words"""
    def __init__(self, words_list, docs_list):
        self.docs = docs_list
        self.graph = dict()
        for word in words_list:
            self.graph[word] = dict()
        
    def coef(self, word, doc):
        """returns the frequency of word in doc"""
        try:
            return self.graph[word][doc]
        except:
            return 0
    
    def doc_contains(self,doc):
        """returns all interesting words in a doc"""
        words_dict = dict()
        for word in self.graph:
            try:
                words_dict[word] = self.graph[word][doc]
            except:
                pass                
        return words_dict
        
    def word_appearance(self, word):
        """returns all frequency of a word"""
        return self.graph[word]

        
    def add_doc(self, docname, dic):
        """Adding all words in dic related to a doc"""
        if docname not in self.docs:
            self.docs.append(docname)
        for word in dic:
            if word not in self.graph:
                self.graph[word] = dict()
            self.graph[word][docname] = dic[word]
                
    def compute_TFIDF(self, word):
        #compute IDF
        appearance = self.word_appearance(word)
        print "\""+word+"\" appears in",len(appearance)," docs."
        idf = log(float(len(self.docs))/len(appearance))
        
        #compute TF * IDF line for a word
        tfidf = dict()
        for doc, freq in appearance.items():
            tfidf[doc] = freq * idf
        return tfidf
            
            
    def pretty_print(self):
        """pretty output"""
        print "\t",
        for doc in self.docs:
            print doc,"|",
        print "\n"
        for word, dic in self.graph.items():
            print word,"|",
            for doc in self.docs:
                if doc in dic.keys():
                    print dic[doc],"|",
                else:
                    print 0,"|",
            print "\n"
            
#until here, 1 line = 1 word, 
# 1 column = 1 doc            
            
    def to_TFIDF_Matrix(self):
        tfidfMatrix = TFIDFMatrix(self.graph.keys(), self.docs)
        for word in self.graph.keys():
            print "Computing for \"",word,"\"..."
            tfidfMatrix.add_word(word, self.compute_TFIDF(word))
        return tfidfMatrix
        
if __name__ == "__main__":
    m = FreqMatrix(["big data", "machine learning", "programming", "operating systems"],
                   ["data science book", "artificial intelligence course", "systems course"])
    m.add_doc("data science book", {"big data":0.5, "machine learning":0.7, "programming":0.5})
    m.add_doc("knuth 101", {"programming":0.45, "operating systems":0.3})
    m.add_doc("artificial intelligence course", {"programming":0.25,"machine learning":0.5})
    m.add_doc("systems course", {"operating systems":0.8, "programming":0.36})
    print m.word_appearance("programming")
    tm = m.to_TFIDF_Matrix()
    tm.pretty_print()
    tm.save("../data/tfidf1.csv")