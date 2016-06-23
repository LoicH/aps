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
import formatConversion
import time


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
        freqMatrix.add_doc(filename[:-8], first)

#frequency matrix is done at this point
freqMatrix.save(data+os.sep+"freq"+time.strftime("%d-%m-%y-%Hh%M")+".csv")
tfidfMatrix = freqMatrix.to_TFIDF_Matrix()

tfidfMatrix.save(data+os.sep+"tfidf"+time.strftime("%d-%m-%y-%Hh%M")+".csv")

#printing a 100 words with the highest TFIDF value
print tfidfMatrix.weights()

#makes the JSon file
formatConversion.convertDict(tfidfMatrix.weights(50), src+os.sep+"templates"+os.sep+"frequency_list.json")

print "All done!"