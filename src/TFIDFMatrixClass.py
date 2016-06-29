# -*- coding: utf-8 -*-
"""
Class handling TFIDF values and storing lots of zeroes (like FreqMatrix)"""

import codecs

class TFIDFMatrix:
    """Contains a graph saving tfidf values of words"""
    def __init__(self):
        self.docs = []
        self.graph = dict()
            
    def add_word(self, word, dic):
        """Add a word in the matrix with the coefficients for each doc
        
        @param word: the word
        @type word: unicode
        
        @param dic: the dictionary containing all doc names (generally ID)
            and their TFIDF value for the word
        @type dic: dict {document name (string): tfidf (float)}
        
        @return: Nothing
        @rtype: None"""
        #print "Adding",word
        if word not in self.graph:
            self.graph[word] = dict()
        for doc, tfidf in dic.items():
            #print "Coef in",doc,"is",tfidf
            if tfidf > 0:
                if doc not in self.docs:
                    self.docs.append(doc)
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
        f = codecs.open(filename, "w","utf-8")
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
        def fit(s):
            if len(s)>=10:
                return s[:9]
            else:
                return s+(9-len(s))*" "
                
        print " "*11,
        for doc in self.docs:
            print fit(str(doc)),"|",
        print "\n"
        for word, dic in self.graph.items():
            print fit(word),"|",
            for doc in self.docs:
                if doc in dic.keys():
                    print fit(str(dic[doc])),"|",
                else:
                    print "    0    ","|",
            print "\n"
            
    def weights(self, number=25):
        """returns the weight of the <number> first words, used for the word cloud.
        The weight of the top word is 100, the weight os the "lowest top word" is 1
        
        @return: a dictionary linking words to their weight
        @rtype: dict {word (unicode): weight(int)}"""
        weights = dict()
        for word in self.graph.keys():
            weights[word] = sum(self.graph[word].values())
        
        l = sorted([(v,k) for (k,v) in weights.items()], reverse=True)[:number-1]
        highest = l[0][0] #highest TFIDF value
        lowest = l [-1][0]
        
        #linear transformation to put the highest value to 100 and the lowest to 1
        if highest-lowest!=0:
            a = (26 -  1)/(highest - lowest)
        else :
            a=26
        b = 1 - a * lowest        
        
        
        return {k:int(a*v+b) for (v,k) in l}
  
    def sum_word(self, word):
            """
            returns the sum of the TFIDF values in the line of  "word" 
            
            """
            return sum(self.graph[word].values())  
  
    def sum_words(self):   
        """returns a dict {word:sum of the TFIDF values in the line} *normalized*"""
        
        Sum = 0
        dic = dict()
        for word in self.graph.keys():
            s = self.sum_word(word)
#            print word,":",s
            Sum += s
            dic[word] = s
#        print "Sum=",Sum
        return {word:(value/Sum) for (word, value) in dic.items()}
  

def analyse_files(file_list, directory):
    """computes the TFIDF Matrix for all the files in directory listed
    by file_list, only if the tfidf.csv is older than the doc.bib
    @param file_list: the list of files you want to examine: ['1234_out.txt',...]
    @type file_list: list of str
    @param directory: the directory of the files: "data"
    @type directory: str
    
    @return: the TFIDF matrix of the top 100 words inside the files
    @rtype: TFIDFMatrix"""
    

           
      
def load(filename):
    """CSV File → Matrix Object"""
    f = open(filename, "r")
    
    #first line = docs
    docs = f.readline() #string = ";d1;d2;d3"
    docs_list = docs.split(",")[1:] #first element = ''
    
    m = TFIDFMatrix()
    
    #then lines = word;tfidf1;tfidf2;... 
    line_str = f.readline()
    while line_str != '':
        line_split = line_str[:-2].split(",") #[:-2] removes '\n'
        word, tfidf_list = line_split[0], line_split[1:]
        dic = dict()
        i = 0
        for value in tfidf_list:
            if value != '' and float(value) > 0:
                dic[docs_list[i]] = float(value)
            i += 1
        m.add_word(word, dic)
        line_str = f.readline()
    return m
    
        
                
            