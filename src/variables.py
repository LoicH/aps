# -*- coding: utf-8 -*-
"""
Module used to share global variables
"""

import os


app_path = os.getcwd().split(os.sep+"aps")[0]+os.sep+"aps"
data_dir = app_path+os.sep+"data"
src_dir = app_path+os.sep+"src"
json_dir = src_dir + os.sep + "static"

if "aps" not in os.listdir('/tmp'):
    os.mkdir("/tmp/aps")
    
tmp_pdf_dir = "/tmp/aps"