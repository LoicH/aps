# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 11:09:45 2016

@author: loic
"""

"""Coding the class of a TFIDF Matrix"""

class TFIDFMatrix:
    """Contains a graph saving tfidf values of words"""
    def __init__(self, words_list, docs_list):
        self.docs = docs_list #words list to link words to index
        self.graph = dict()
        for word in words_list:
            self.graph[word] = dict()
            
    def add_word(self, word, dic):
        """adds a word with his dictionary {doc:tfidf by doc}"""
        if word not in self.graph:
            self.graph[word] = dict()
        for doc, tfidf in dic.items():
            self.graph[word][doc] = tfidf
            
    def add_doc(self, doc, dic):
        """adds a doc with his dictionary {word:tfidf by word}"""
        if doc not in self.docs:
            self.docs.append(doc)
        for word in dic:
            if word not in self.graph:
                self.graph[word] = dict()
            self.graph[word][doc] = dic[word]
    
    def save(self, filename):
        """saves the matrix under the csv format"""
        f = open(filename, "w")
        for doc in self.docs:
            f.write(","+doc)
        for word, dic in self.graph.items():
            f.write("\n")
            f.write(word)
            for doc in self.docs:
                if doc in dic:
                    f.write(","+str(dic[doc]))
                else:
                    f.write(",0")
        f.close()
    
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

def load(filename):
    m = TFIDFMatrix([], [])
    f = open(filename, "r")
    
    #first line = docs
    docs = f.readline() #string = ";d1;d2;d3"
    docs_list = docs.split(",")[1:] #first element = ''
    
    m = TFIDFMatrix([],docs_list)
    
    #then lines = word;tfidf1;tfidf2;... 
    line_str = f.readline()
    while line_str != '':
        line_split = line_str[:-2].split(",") #[:-2] removes '\n'
        word, tfidf_list = line_split[0], line_split[1:]
        dic = dict()
        i = 0
        for value in tfidf_list:
            if value > 0:
                dic[docs_list[i]] = value
            i += 1
        m.add_word(word, dic)
        line_str = f.readline()
    return m
    


if __name__ == "__main__":
    m = load("tfidf1.csv")
    m.pretty_print()
        
                
            