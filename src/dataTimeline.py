# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 10:43:42 2016

@author: asueur
"""
from freqMatrixClass import FreqMatrix
from retrieveCategories import getAll
from timelineVisualization import getInfo
from Timeline import formatDate
from TFIDFMatrixClass import TFIDFMatrix
import initServer
import pdf2txt
import PDFdl

import os
from requests.exceptions import HTTPError
from datetime import date

app_path = os.getcwd().split(os.sep+"aps")[0]+os.sep+"aps"
data = app_path+os.sep+"data"

def getCategories(filepath):
    """
    returns the frequencies of categories in a file.
    @param filepath: the path to the text file
    @type filepath: str
    
    @return: a dictionary {category:frequency}
    @rtype: dict {str:float}
    """
    fileName=open(filepath,"r")
    fileText = fileName.read()
    fileName.close()
    #freq_dictionaries[title]=getAll(fileText)[0] #category frequencies of documents
    try:
        return getAll(fileText)[0]
    except HTTPError as e:
        print 'Error getting categories for %s: "%s"'% (filepath, e.message)
        return dict()
    
def createTFIDFMatrix(authorName, startDateString, endDateString): #date format: year monthNumber
    """ create TFIDF Matrix using documents written by an author during a selected period
    @param authorName: author's lastname
    @type authorName: string
    
    @param startDateString: start of the period you want to select
    @type startDateString: string "year monthNumber"
    
    @param endDateString: end of the period you want to select
    @type endDateString: string "year monthNumber"
    
    @return: TFIDF Matrix using documents selected
    @rtype: TDIDFMatrix object """
     
    #dictionary of frequency dictionaries for documents {id: {category:frequency}}
    #freq_dictionaries = dict()
    
    
    #dictonary of publications, dates and ids e.g: {pubName: [date,id]}
    title_dict = getInfo(authorName)[0]    
    
    #dictionary of publications {pubname:id} only for those in the selected time interval
    titleId = dict()
    
    #selecting the titles inside de time period
    for title, [dateString, pdf_id] in title_dict.items():
        formatedDate=formatDate(dateString)
        #formatedDate = "2015 02"
        
        pubDate=date(int(formatedDate.split()[0]),int(formatedDate.split()[1]),1)
        #pubDate = date object : (2015, 2, 1) or 1st feb. 2015
        
        #converting the date arguments from string to date objects
        formatedStart = formatDate(startDateString)
        startDate = date(int(formatedStart.split()[0]),int(formatedStart.split()[1]),1)
        formatedEnd = formatDate(endDateString)
        endDate = date(int(formatedEnd.split()[0]),int(formatedEnd.split()[1]),1)
        
        #checks if text was published in a fixed time window        
        if pubDate >= startDate and pubDate < endDate: 
            titleId[title] = pdf_id
    

    #construting the frequency matrix for the concerned documents        
    fm=FreqMatrix([],[])
    for title, pdf_id in titleId.items():
        print pdf_id
        
        #Trying to get the data from this pdf:
        
        #the text is already extracted from the PDF
        if str(pdf_id)+"_out.txt" in os.listdir(data):
            fm.add_doc(pdf_id, getCategories(initServer.data+os.sep+str(pdf_id)+"_out.txt"))
        
        #the PDF is downloaded but no text is extracted
        elif str(pdf_id)+".pdf" in os.listdir(initServer.tmp_pdf_dir):
            print "File "+str(pdf_id)+"_out.txt not found in data directory" ,
            print "But the PDF is in temporary directory."
            pdf2txt.pdf_to_file(initServer.tmp_pdf_dir+os.sep+str(pdf_id)+".pdf",
                                    initServer.data+str(pdf_id)+"_out.txt")
            os.remove(initServer.tmp_pdf_dir+os.sep+str(pdf_id)+".pdf")
            fm.add_doc(pdf_id, getCategories(initServer.data+os.sep+str(pdf_id)+"_out.txt"))

        #the PDF hasn't been downloaded at all
        else:
            print "No txt file nor pdf, trying to download."
            try:
                PDFdl.downloadPDF(pdf_id, initServer.tmp_pdf_dir, initServer.data)
                pdf2txt.pdf_to_file(initServer.tmp_pdf_dir+os.sep+str(pdf_id)+".pdf",
                                    initServer.data+str(pdf_id)+"_out.txt")
                os.remove(initServer.tmp_pdf_dir+os.sep+str(pdf_id)+".pdf")
                fm.add_doc(pdf_id, getCategories(initServer.data+os.sep+str(pdf_id)+"_out.txt"))
            except:
                print 'Error downloading the file'
            
                
      
    return fm.to_TFIDF_Matrix()

def median(matrixList): 
    """
    returns average value of category frequencies for multiple TFIDF matrixes
    return type : dictionary {word:float}
    """
    n=len(matrixList) #number of matrixes
    totalFreq=dict()
    dictList=[]  #list of all the total frequency dictionaries from the matrixes
    for m in matrixList:
        m.pretty_print()
        wordDict=m.sum_words()
        dictList.append(wordDict)
    wordList=[] #list of all possible categories/words
    for d in dictList:
        for word in d.keys():
            if word not in wordList:
                wordList.append(word)
    for word in wordList:
        for d in dictList:
            if word in d:
                if word in totalFreq:
                    totalFreq[word]+=d[word]
                else:
                    totalFreq[word]=d[word]
    for i in totalFreq:
        totalFreq[i]=totalFreq[i]/float(n)
    return totalFreq
        

if __name__ == "__main__":
    createTFIDFMatrix("C. Concolato", "2012 jan", "2015 dec").pretty_print()
    
    