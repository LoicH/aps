# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 16:27:21 2016

@author: asueur
"""

import os
import re
import pdf2txt
import retrieveCategories
import dataTimeline
import sys
import Timeline
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import formatConversion
from calendar import monthrange
import PDFdl

bibName="testbib.bib"
entries=PDFdl.openBibLib(bibName).entries 

#argv must be: main authorName startDate endDate periodLength(in months)
app_path = os.getcwd().split(os.sep+"aps")[0]+os.sep+"aps"
data = app_path+os.sep+"data"
src = app_path+os.sep+"src"

def monthdelta(d1, d2):
    delta = 0
    while True:
        mdays = monthrange(d1.year, d1.month)[1]
        d1 += timedelta(days=mdays)
        if d1 <= d2:
            delta += 1
        else:
            break
    return delta




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


#Constructing TFIDFMatrixes for every concerned time period
periodFrequenciesList=[]
matrixList=[]
authorName=sys.argv[1]
startDate=Timeline.formatDate(sys.argv[2])
endDate=Timeline.formatDate(sys.argv[3])
startDateTime=date(int(str(startDate).split()[0]),int(str(startDate).split()[1]),1) #conversion to objects of type dateTime
endDateTime=date(int(str(endDate).split()[0]),int(str(endDate).split()[1]),1)
periodLength=int(sys.argv[4])
periodNumber2=monthdelta(startDateTime,endDateTime)//periodLength #number of periods considered
date1=startDateTime
date2=date1+ relativedelta(months=+periodLength)

for i in range(periodNumber2+1):  #create TFDIDF Matrixes for each period
    print i
    m=dataTimeline.createTFIDFMatrix(authorName, date1, date2) #TFIDF Matrix with all words/concepts.
#    tops = m.weights(number=5) #dictionary {concept:weight} for the top 5 five concepts, weight of best concept = 100, least = 1
    matrixList.append(m)
    date1=date2
    date2=date1+ relativedelta(months=+periodLength)
periodFrequenciesList.append(dataTimeline.median([matrixList[0],matrixList[1]]))                                    # 
if periodNumber2>=2:                                                                                                # create period 
    for i in range(1,periodNumber2):                                                                              # frequency List
        periodFrequenciesList.append(dataTimeline.median([matrixList[i-1],matrixList[i],matrixList[i+1]]))          #
periodFrequenciesList.append(dataTimeline.median([matrixList[-2],matrixList[-1]]))

#selecting the 10 best words

#computing the scores
scores = dict() #{word: score}
for dic in periodFrequenciesList:
    for word, frequency in dic.items():
        if word in scores.keys():
            scores[word] += frequency
        else:
            scores[word] = frequency

#selecting the best:
sorted_items = sorted([(score, word) for (word, score) in scores.items()], reverse=True)[:9]
best_words = [word for (score, word) in sorted_items]
#filtering the periodFrequenciesList to keep only the best words:
filteredFrequenciesList = []
for old_dic in periodFrequenciesList:
    filtered_dic = dict()
    for word, frequency in old_dic.items():
        if word in best_words:
            filtered_dic[word] = frequency
    filteredFrequenciesList.append(filtered_dic)


periodFreqJSON=formatConversion.convertToMatrice(filteredFrequenciesList, src+os.sep+"templates"+os.sep+"timeline.json", periodNumber2) #converting to output format

      # test: python main_timeline.py "Concolato" "2015 jan" "2016 jan" 6        