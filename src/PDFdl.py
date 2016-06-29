# -*- coding: utf-8 -*-
"""
Used to download PDF files
"""

import urllib
import re
import bibtexparser

#converts weird char in the bibtex file
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode

import os

import variables 

regex=r'id=(\d+)'  

def openBibLib(bibName): 
    """Extracts the corpus information from a bibtex file
    
    @param bibName: the path to the file
    @type bibName: string
    
    @return: the BibDatabase object with all the information
    @rtype: BibDatabase"""
    with open(bibName) as bibtex_file:  
        parser = BibTexParser()
        parser.customization = convert_to_unicode
        bibtex_database = bibtexparser.load(bibtex_file, parser=parser) 
    return bibtex_database


#def download(fileURL,writeFile):
#    testfile = urllib.URLopener()
#    try:
#        testfile.retrieve(fileURL, writeFile)  # example: testfile.retrieve("http://biblio.telecom-paristech.fr/cgi-bin/download.cgi?id=11068", "file.pdf")
#    except IOError:
#        print "No pdf or no memory left"

def downloadPDF(pdf_id, pdf_out_dir, txt_out_dir):
    """downloads the pdf with a given ID and puts it into pdf_out_dir
    if the "pdf"_out.txt is not in txt_out_dir
    
    @param pdf_id: the ID of the doc
    @type pdf_id: str
    
    @param pdf_out_dir: the directory where you want to put the pdf files (e.g. /tmp/aps/)
    @type pdf_out_dir: str
    
    @param txt_out_dir: the directory where the *_out.txt are
    @type txt_out_dir: str
    """
    try:
        os.mkdir(pdf_out_dir)
    except:
        "Error creating the temporary PDF folder"
    testfile = urllib.URLopener()
    print  "Examinating PDF n°"+str(pdf_id)
    try:
        if str(pdf_id)+".pdf" in os.listdir(pdf_out_dir): 
        #checks if the file already exists
            print str(pdf_id)+".pdf already downloaded"
        elif str(pdf_id)+"_out.txt" in os.listdir(txt_out_dir):
            print "The text from %s is already extracted." %  str(pdf_id)+".pdf"
        else:
            print "Trying to download the file"
            testfile.retrieve("""http://biblio.telecom-paristech.fr/cgi-bin/download.cgi?id="""
            +str(pdf_id), pdf_out_dir+os.sep+str(pdf_id)+".pdf")
    except IOError as e:
        print "No pdf or no memory left (Error message: \"%s\")." % e
        raise e
        

def downloadAll(bibName, pdf_out_dir, txt_out_dir): 
    """downloads all files from a given bibTex library 
    and puts them into out_dir if the "pdf"_out.txt is not in txt_out_dir
    @param bibName: the path of the bibtex file
    @type bibName: str
    
    @param pdf_out_dir: the directory where you want to put the pdf files (e.g. /tmp/aps/)
    @type pdf_out_dir: str
    
    @param txt_out_dir: the directory where the *_out.txt are
    @type txt_out_dir: str
    
    @return: a dictionary {position in bibtex:id of pdf}
    @rtype: dict
    """
    pos_Id_List = dict()
    print "Opening the bib file...",
    bibtex_database=openBibLib(bibName)
    print "done."
    for i in range(len(bibtex_database.entries)):
        try:
            annote=bibtex_database.entries[i]["annote"]
        except KeyError:
            print "No id found"
        print i
        pdf_id=int(re.findall(regex,annote)[0])
        try:
            downloadPDF(pdf_id, pdf_out_dir, txt_out_dir)
            pos_Id_List[i]=pdf_id
        except IOError:
            pass
    return pos_Id_List
    
if __name__ == "__main__":
    downloadAll(variables.data_dir+os.sep+"concolato.bib", 
                variables.tmp_pdf_dir, variables.data_dir)