# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 15:55:42 2016

@author: AntoineTelecom
"""
import sys
import os      #file manipulation
import codecs  #write files in utf8
import fnmatch #to match filename and implement testing
import nltk    #words retriever
import random  #used for testing



#import subprocess
#s="python pdf2txt.py TP3.pdf"
#proc = subprocess.Popen("ls", stdout=subprocess.PIPE)
#
#proc = subprocess.Popen("python pdf2txt.py TP3.pdf", stdout=subprocess.PIPE)
#tmp = proc.stdout.read()
#print tmp

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

app_path = os.getcwd().split(os.sep+"aps")[0]+os.sep+"aps"
data = app_path+os.sep+"data"
src = app_path+os.sep+"src"

def pdf_to_txt(path):
    """converts pdf into a string
    @param path : path to the file
    @type path : string
    
    @return: pdf content
    @rtype: string"""
    
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec='utf-8', laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    s = retstr.getvalue()
    retstr.close()
    return s
    
def pdf_to_file(src_filepath, out_filepath):
    """Outputs a file to out_filepath   
    @return: pdf content
    @rtype: txt file"""
    print "Processing...",
    raw_txt = pdf_to_txt(src_filepath)
    src_filename = src_filepath.split(os.path.sep)[-1] #with .pdf at the end
    docname = src_filename.split(".")[0] #doc name without .pdf
    output = codecs.open(app_path+"/data/"+docname+"_out.txt", "w", "utf-8")
    output.write(raw_txt.decode('utf-8'))
    output.close()
    print "Done."

def testing():
    """Tests all the sample files in the current directory
    """
    trials = 1000
    print "Testing for", trials,"words."
    for filename in os.listdir(app_path+'/data/'):
        if fnmatch.fnmatch(filename, '*_orig.txt'):
            docname = filename[:-9]
            print "Testing ",docname,"..."
            if test_file(docname, trials):
                print "Done."
            else:
                print "ERROR."
                break
            

def test_file(docname, trials):
    """Tests a sample file to check the integrity"""
    src_file = codecs.open(app_path+"/data/"+docname+"_orig.txt", 'r', "utf-8")
    src_txt = src_file.read() #src_txt is unicode
    src_file.close()

    dest_txt = pdf_to_txt(app_path+"/data/"+docname+".pdf").decode("utf-8") #unicode
    words_src = nltk.word_tokenize(src_txt)
    count = 0
    for i in range(trials):
        chosen_word = random.choice(words_src)
        if chosen_word in dest_txt:
            count += 1
#        else :
#            print chosen_word,"not in destination"
    print "Success rate:",float(count)/trials
    return (float(count)/trials >= 0.7)
        
    
    

if __name__ == '__main__':
    sys.path.append("/usr/home/username/pdfminer") #? what's the use?

    app_path = os.getcwd().split(os.sep+"aps")[0]+os.sep+"aps"
    
    
    """Adding arguments for command-line use"""
    import argparse
    parser = argparse.ArgumentParser(description='Convert PDF to text')
    parser.add_argument('-f','--file', help="source file")
    parser.add_argument('-o', '--output', help="output file")
    parser.add_argument('-t', '--testing', help="""runs on sample files, it's the action 
            by default if you invoke this script without arguments""", action="store_true")
    
    args = parser.parse_args()
    if args.file :
        pdf_to_file(args.file, args.output)
    elif args.testing :
        testing()
        

