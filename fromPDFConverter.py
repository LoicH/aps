# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 15:55:42 2016

@author: asueur
"""
import sys
import os   
sys.path.append("/usr/home/username/pdfminer")
path ="/cal/homes/asueur/Downloads/pdfminer-20140328/samples/simple1.pdf"

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

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
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
    

a= convert_pdf_to_txt("TP3.pdf")