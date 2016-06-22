# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 17:19:28 2016

@author: loic
"""

import os
#import fnmatch
import re
import pdf2txt
import modifTexte
from freqMatrixClass import FreqMatrix

app_path = os.getcwd().split(os.sep+"aps")[0]+os.sep+"aps"
data = app_path+os.sep+"data"
src = app_path+os.sep+"src"


#Getting the text from all PDF 
print "Getting the text from the PDF"
for filename in os.listdir(data):
    matchObj = re.match(r'(.*)\.pdf', filename)
    if matchObj:
        try:
            docname = matchObj.group(1)
            if docname+"_out.txt" not in os.listdir(data):
                print "Retrieving text of",docname
                pdf2txt.pdf_to_file(data+os.sep+filename, data+os.sep+docname+"_out.txt")
        except:
            print "Problem getting the name of the file \"",filename,"\"."


#Constructing frequency dictionary for all documents
freqMatrix = FreqMatrix([],[])

def get_first(dic, n):
    """Returns a dic of the first n terms, sorted by value"""
    output_dic = dict()
    for value in sorted(dic.values())[:n-1]:
        output_dic[dic.get(value)] = value
        dic.pop(dic.get(value))
    return output_dic
    
print "Analyzing text of PDF"

for filename in os.listdir(data):
    if re.match(r'(.*)_out\.txt', filename):
        print filename
        f = open(data+os.sep+filename, 'r')
        txt = f.read()
        f.close()
        dic = modifTexte.textToDictionnary(txt.decode("utf-8"),[])
        l = sorted([(v,k) for (k,v) in dic.items()], reverse=True)[:99]
        first = {k:v for (v,k) in l}
        print first
        freqMatrix.add_doc(filename[:-8], first)

freqMatrix.pretty_print()

        
    