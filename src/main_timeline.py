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
from datetime import date
from dateutil.relativedelta import relativedelta
import formatConversion

#argv must be : main authorName startDate endDate periodLength(in months)

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


#Constructing TFIDFMatrixes for every concerned time period
periodFrequenciesList=[]
matrixList=[]
authorName=sys.argv[1]
startDate=Timeline.formatDate(sys.argv[2])
endDate=Timeline.formatDate(sys.argv[3])
startDateTime=date(int(startDate.split()[0]),int(startDate.split()[1]),1) #conversion to objects of type dateTime
endDateTime=date(int(endDate.split()[0]),int(endDate.split()[1]),1)
periodLength=int(sys.argv[4])
#monthNumber=(endDate.split()[0]-startDate.split()[0])*12 +endDate.split()[1]-startDate.split()[1]
#periodNumber=monthNumber//periodLength 
periodNumber2=(endDateTime-startDateTime).days//31//periodLength #number of periods considered
date1=date(int(startDate.split()[0]),int(startDate.split()[1]),1)
date2=date1+ relativedelta(months=+periodLength)
for i in range(periodNumber2):  #create TFDIDF Matrixes for each period
    matrixList.append(dataTimeline.createTFIDFMatrix(authorName, date1, date2))
    date1=date2
    date2=date1+ relativedelta(months=+periodLength)
periodFrequenciesList.append(dataTimeline.median([matrixList[0],matrixList[1]]))                                    # 
if periodNumber2>=2:                                                                                                # create period 
    for i in range(1,periodNumber2-1):                                                                              # frequency List
        periodFrequenciesList.append(dataTimeline.median([matrixList[i-1],matrixList[i],matrixList[i+1]]))          #
periodFrequenciesList.append(dataTimeline.median([matrixList[-2],matrixList[-1]]))                                  #
print periodFrequenciesList
periodFreqJSON=formatConversion.convertToMatrice(periodFrequenciesList, src+os.sep+"templates"+os.sep+"timeline.json", periodNumber2) #converting to output format
print periodFreqJSON
       