# -*- coding: utf-8 -*-
"""
Performs computations for the timeline (moving average, TFIDF matrix creation)
"""

import os
from requests.exceptions import HTTPError
from datetime import date
import re


from freqMatrixClass import FreqMatrix
from retrieveCategories import getAll
from timelineVisualization import getInfo
import initServer
import pdf2txt
import PDFdl

import variables

def formatMonth(string):
    """ converts from number to month"""
    switcher = { "jan": "01","feb": "02", "mar": "03", "apr": "04","may": "05", "jun": "06", "jul": "07", "aug": "08", "sep": "09", "oct": "10", "nov": "11", "dec": "12" }      
    return switcher.get(string)
    
def formatDate(string): 
    """turns "2015 feb" into "2015 02" for instance"""
    
    matchObject = re.search(r"(\d+) ([a-zA-Z]+)", string)    
    if matchObject:        # return 0 if the string doesn't match
        date = matchObject.group(0)
        month = matchObject.group(2)
        return date.replace(month, formatMonth(month))
    else:
        print "The date is wrongly formatted, can't convert it."
        return 0

def getCategories(filepath):
    """
    returns the frequencies of categories in a file.
    @param filepath: the path to the text file
    @type filepath: string
    
    @return: a dictionary {category:frequency}
    @rtype: dict {str:float}
    """
    fileName=open(filepath,"r")
    fileText = fileName.read()
    fileName.close()

    try:
        return getAll(fileText)[0]
    except HTTPError as e:
        print 'Error getting categories for %s: "%s"'% (filepath, e.message)
        return dict()
    
def createTFIDFMatrix(authorName, startDate, endDate, bibName):
    """
    create TFIDF Matrix using documents written by an author 
    during a selected period
        
    @param authorName: author's lastname
    @type authorName: string
    
    @param startDate: start of the period you want to select
    @type startDate: datetime.date
    
    @param endDate: end of the period you want to select
    @type endDate: datetime.date
    
    @param bibName: the path to the corpus
    @type bibName: string 
    
    @return: TFIDF Matrix using documents selected
    @rtype: TDIDFMatrix object """
     
    #dictionary of frequency dictionaries for documents {id: {category:frequency}}
    #freq_dictionaries = dict()
    
    
    #dictonary of publications, dates and ids e.g: {pubName: [date,id]}
    title_dict = getInfo(authorName, bibName)[0]    
    
    #dictionary of publications {pubname:id} only for those in the selected time interval
    titleId = dict()
    
    #selecting the titles inside de time period
    for title, [dateString, pdf_id] in title_dict.items():
        formatedDate=formatDate(dateString)
        #formatedDate = "2015 02"
        
        pubDate=date(int(formatedDate.split()[0]),int(formatedDate.split()[1]),1)
        #pubDate = date object : (2015, 2, 1) or 1st feb. 2015
        
        #checks if text was published in a fixed time window        
        if pubDate >= startDate and pubDate < endDate: 
            titleId[title] = pdf_id
    

    #construting the frequency matrix for the concerned documents        
    fm=FreqMatrix()
    for title, pdf_id in titleId.items():
        print pdf_id
        
        #Trying to get the data from this pdf:
        
        #the text is already extracted from the PDF
        if str(pdf_id)+"_out.txt" in os.listdir(variables.data_dir):
            fm.add_doc(pdf_id, getCategories(
                variables.data_dir+os.sep+str(pdf_id)+"_out.txt"))
        
        #the PDF is downloaded but no text is extracted
        elif str(pdf_id)+".pdf" in os.listdir(variables.tmp_pdf_dir):
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
            
                
    fm.pretty_print()
    return fm.to_TFIDF_Matrix()

def median(matrixList): 
    """
    returns average value of category frequencies for multiple TFIDF matrixes
    
    @param matrixList: the list of matrices you want the average
    @type matrixList: TFIDFMatrix list
    
    @return: a dictionary linking words to their weight
    @rtype: dict {unicode: float}
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
    start = date(2012, 1, 1)
    end = date(2015, 12, 1)
    t = createTFIDFMatrix("C. Concolato", start, end, 
                      variables.data_dir + os.sep + "concolato.bib")
    
    