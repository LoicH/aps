# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 11:53:50 2016

@author: loic
"""

"""Populating the database and performing the calculations"""

import PDFdl
import os
import pdf2txt
import TFIDFMatrixClass
import time
import formatConversion

app_path = os.getcwd().split(os.sep+"aps")[0]+os.sep+"aps"
data = app_path+os.sep+"data"
src = app_path+os.sep+"src"
tmp_pdf_dir = "/tmp/aps"

def extract_text(bibtex):
    """Download the files in the bibtex, extracts the text from the files
    @param bibtex: the complete filepath of the bibtex file
    @type bibtex: str
    
    @return: nothing"""
    
    print "Downloading the files...",
    #the theoritical pdf files downloaded from the bibtex:
    pdf_ids_list = PDFdl.downloadAll(bibtex, tmp_pdf_dir, data).values()
    print "done."
    print "Getting the text from the PDF..."
    for pdf_id in pdf_ids_list:
        print "PDF id =",pdf_id,
        if str(pdf_id)+"_out.txt" in os.listdir(data):
            print "is already in data folder"
        else:
            pdf2txt.pdf_to_file(tmp_pdf_dir+os.sep+str(pdf_id)+".pdf", data+os.sep+str(pdf_id)+"_out.txt")
    return pdf_ids_list

def make_json_wordcloud2(bibtex):
    """makes a TFIDF matrix from the pdf in the bibtex, then extracts a JSON
    file for visalization"""
    pdf_id_list = extract_text(bibtex)
    print "Text extracted, PDF ID list =",pdf_id_list
    print "Creating the TFIDF Matrix...",
    t = TFIDFMatrixClass.analyse_files([str(pdf_id)+"_out.txt" for pdf_id in pdf_id_list], data)
    print "done."    
    t.save(data+os.sep+"tfidf"+time.strftime("%d-%m-%y-%Hh%M")+".csv")
    print "Saving the JSON file"
    formatConversion.convertDict2(t.weights(50), 
        src+os.sep+"static"+os.sep+"wordcloud"+os.sep+"tags.json")
    print "All done!"
                        
        
    

if __name__ == "__main__":
    make_json_wordcloud2(data+os.sep+"concolato.bib")
    