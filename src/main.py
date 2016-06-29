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


##Getting the text from all PDF 
print "Getting the text from the PDF"

#get all the PDF files
files = os.listdir(data)
pdfs = []
for filename in files:
    matchObj = re.match(r'(.*)\.pdf', filename)
    if matchObj:
        pdfs.append(matchObj.group(1))

count = 0
total = len(pdfs)
for docname in pdfs:
    count += 1
    print "(",count,"/",total,")"
    try:
        if docname+"_out.txt" not in os.listdir(data):
            print "Retrieving text of",docname
            pdf2txt.pdf_to_file(data+os.sep+filename, data+os.sep+docname+"_out.txt")
    except:
        print "Problem opening \"",filename,"\"."


#Constructing frequency dictionary for all documents
freqMatrix = FreqMatrix([],[])

    
print "Analyzing text of PDF"
out_txts = []
for filename in files:
    matchObj = re.match(r'(.*)_out\.txt', filename)
    if matchObj:
        out_txts.append(filename)
count = 0
total = len(out_txts)
not_english = []
for filename in out_txts:
    count += 1
    print "(",count,"/",total,")"
    print filename
    f = open(data+os.sep+filename, 'r')
    txt = f.read()
    f.close()
    if modifTexte.estimate_language(txt) == 'english':
        dic = modifTexte.textToDictionnary(txt.decode("utf-8"),[])
        l = sorted([(v,k) for (k,v) in dic.items()], reverse=True)[:99]
        first = {k:v for (v,k) in l}
        freqMatrix.add_doc(filename[:-8], first)
    else:
        print filename,"is not in english!"
        not_english.append(filename)

print "Docs not in english:",not_english

#frequency matrix is done at this point
freqMatrix.save(data+os.sep+"freq"+time.strftime("%d-%m-%y-%Hh%M")+".csv")
tfidfMatrix = freqMatrix.to_TFIDF_Matrix()

tfidfMatrix.save(data+os.sep+"tfidf"+time.strftime("%d-%m-%y-%Hh%M")+".csv")

#printing a 100 words with the highest TFIDF value
print tfidfMatrix.weights()

#makes the JSon file
weights=tfidfMatrix.weights(50)
formatConversion.convertDict2(weights, src+os.sep+"templates"+os.sep+"wordcloud"+os.sep+"tags.json")

print "All done!"