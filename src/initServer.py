# -*- coding: utf-8 -*-
"""
Creates the JSON files for visualization from bibtex files
The server will call the functions make_json_timeline and make_json_wordcloud2
to create the JSON files when needed"""

import os
import codecs
import threading 
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from calendar import monthrange

app_path = os.getcwd().split(os.sep+"aps")[0]+os.sep+"aps"
data = app_path+os.sep+"data"
src = app_path+os.sep+"src"
tmp_pdf_dir = "/tmp/aps"

import pdf2txt
import TFIDFMatrixClass
import freqMatrixClass
import PDFdl
import modifTexte
import formatConversion
import dataTimeline





def _compute_tfidf(bib_path):
    """
    Saves a "bibtex"_tfidf.csv with a given bibtex file, only if the .csv is older 
    than the .bib.
        
        >>> t = compute_tfidf("data/document.bib")

    @param bib_path: the complete filepath of the bibtex file
    @type bib_path:  string   

    @return: The TFIDF Matrix 
    @rtype: TFIDFMatrix
    
    """
    
    #bib_path = "/home/user/aps/data/document.bib" → bib_name = "document"
    bib_name = bib_path.split(os.sep)[-1][:-4]    
    
    csv_name = bib_name + "_tfidf.csv"  # "document_tfidf.csv"
    csv_path = data + os.sep + csv_name # "/home/user/aps/data/document_tfidf.csv"
    
    #if the .csv is newer than the .bib file, don't bother re-computing the TFIDF matrix
    if csv_name in os.listdir(data) and os.path.getctime(csv_path) > os.path.getctime(bib_path) :
        print "I already computed the TFIDF for this bibtex!"
        tmatrix = TFIDFMatrixClass.load(csv_path)
    
    else:
        #Downloading the PDF file
        print "Downloading the files...",
        #the theoritical pdf files downloaded from the bibtex:
        pdf_ids_list = PDFdl.downloadAll(bib_path, tmp_pdf_dir, data).values()
        print "done."
        
        #Extract the text out of PDF
        print "Getting the text from the PDF..."
        for pdf_id in pdf_ids_list:
            print "PDF id =",pdf_id,
            if str(pdf_id)+"_out.txt" in os.listdir(data):
                print "is already in data folder"
            else:
                pdf2txt.pdf_to_file(tmp_pdf_dir+os.sep+str(pdf_id)+".pdf", data+os.sep+str(pdf_id)+"_out.txt")
                os.remove(tmp_pdf_dir+os.sep+str(pdf_id)+".pdf")
        
        #Create the frequency matrix for the docs
        fmatrix = freqMatrixClass.FreqMatrix([],[])
        for pdf_id in pdf_ids_list:
            f = codecs.open(data+os.sep+str(pdf_id)+"_out.txt", 'r', "utf-8")
            txt = f.read()
            f.close()
            dic = modifTexte.textToDictionnary(txt,[])
            l = sorted([(v,k) for (k,v) in dic.items()], reverse=True)[:99]
            top_words = {k:v for (v,k) in l}
            fmatrix.add_doc(str(pdf_id), top_words)
        
        #Converting into a TFIDF matrix and saving it in the CSV file
        tmatrix = fmatrix.to_TFIDF_Matrix()
        tmatrix.save(csv_path)
        
    return tmatrix
    

def make_json_wordcloud2(bibtex):
    """
    Creates a JSON file from a bibtex file to visualize the 2nd version 
    of the wordcloud.
    
    @param bibtex: the path to the bibtex file
    @type bibtex: string
    
    @return: Nothing
    @rtype: None
    """
    tmatrix = _compute_tfidf(bibtex)
    print "Saving the JSON file"
    formatConversion.convertDict2(tmatrix.weights(50), 
        src+os.sep+"static"+os.sep+"wordcloud"+os.sep+"tags.json")
    print "All done!"
  

def _monthdelta(d1, d2):
    """
    Computes the months difference between two dates
    
    @param d1: the first date
    @type d1: date object
    
    @param d2: the second date
    @type d2: date object
    
    @return: the number of months between the two dates
    @rtype: int
    """
    delta = 0
    while True:
        mdays = monthrange(d1.year, d1.month)[1]
        d1 += timedelta(days=mdays)
        if d1 <= d2:
            delta += 1
        else:
            break
    return delta
            
def _select_top_timeline(freq_list, number=10):
    """
    Returns the frequency list, but only with the best words, i.e. the words
    that have the biggest sum of frequencies.
    
    @param freq_list: the list of dictionaries {word:frequency}
    @type freq_list: dictionary {word (str or unicode?):float}
    
    @param number: the number of words you want
    @type number: int
    
    @return: the list of dictionaries {word:frequency} reduced to the top words
    @rtype: dictionary {word:float} (same as freq_list)"""   
    
    scores = dict()
    for dic in freq_list:
        for word,freq in dic.items():
            if word in dic.keys():
                scores[word] += freq
            else:
                scores[word] = freq
                
    #the top words:
    top_words = sorted([k for (k,v) in scores.items()], reverse=True)[:number-1]
    
    #we copy freq_list in return_freq_list selecting only the top words
    return_freq_list = []
    for old_dic in freq_list:
        new_dic = dict()
        for word, freq in old_dic.items():
            if word in top_words:
                new_dic[word] = freq
        return_freq_list.append(new_dic)
   
    return return_freq_list
                
        
   
    
def make_json_timeline(authorName, startDate, endDate, periodLength, json_filepath):
    """Creates a JSON file for a timeline about a given author between two dates.
    
        >>> make_json_timeline("J. Doe", "2012 jan", "2015 dec", "src/static/timeline/timeline.json")
    
    @param authorName: The name of the author you want to visualize, 
        must respect the case: "J. Doe"
    @type authorName: unicode
    
    @param startDate: The date where you want to start : "2012 jan"
    @type startDate: string

    @param endDate: The date where you want to stop.
    @type endDate: string
 
    @param periodLength: Number of months between two steps.
    @type periodLength: int

    @param json_filepath: Complete path of the JSON output: "src/static/timeline/timeline.json"
    @type json_filepath: string
    
    @return: Nothing
    @rtype: None
    
    """
    periodFrequenciesList = []
    #periodFrequenciesList will save moving average (French: « moyenne glissante »)
    # for every data point
    
    matrixList = []
    #matrixList will save every TFIDF matrix for every period


    #conversion to objects of type datetime.date
    startDateTime = date(int(startDate.split()[0]), int(startDate.split()[1]), 1) 
    endDateTime = date(int(endDate.split()[0]), int(endDate.split()[1]), 1)
    
    #number of periods considered
    periodsNumber = _monthdelta(startDateTime,endDateTime)//periodLength 
    
    #create TFDIDF Matrixes for each period
    date1 = startDateTime
    rdelta = relativedelta(months=+periodLength)
    date2 = date1 + rdelta
    for i in range(periodsNumber + 1):  
    
        #TFIDF Matrix with all words/concepts:
        tfidfMatrix = dataTimeline.createTFIDFMatrix(authorName, date1, date2) 

        matrixList.append(tfidfMatrix)
        
        date1=date2
        date2=date1 + rdelta
        
    #first data point, we can only compute an average on 2 data points
    periodFrequenciesList.append(dataTimeline.median([matrixList[0],matrixList[1]]))                                     
    if periodsNumber>=2:                                                                                                 
        for i in range(1,periodsNumber):       
            #computing moving average on 3 data points                                                                      
            periodFrequenciesList.append(dataTimeline.median([matrixList[i-1],matrixList[i],matrixList[i+1]]))          
    
    #last data point:
    periodFrequenciesList.append(dataTimeline.median([matrixList[-2],matrixList[-1]]))
    
    topFrequenciesList = _select_top_timeline(periodFrequenciesList, number=10)
    
    #converting to output format
    formatConversion.convertToMatrice(topFrequenciesList, 
        src+os.sep+"templates"+os.sep+"timeline.json", periodsNumber) 


        
    

if __name__ == "__main__":
    threading.Thread(PDFdl.downloadAll(data+os.sep+"document.bib",tmp_pdf_dir,data)).start()
    make_json_wordcloud2(data+os.sep+"concolato.bib")
    make_json_timeline("C. Concolato", "2012 01", "2015 12", 6, 
        src+os.sep+"static"+os.sep+"timeline"+os.sep+"timeline.json")