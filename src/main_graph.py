# -*- coding: utf-8 -*-
"""
Work flow used to create the co-authoring graph
"""

from dataGraph import getdictCoauthors
from formatConversion import convertGraph
import PDFdl
import variables
import os

bibName = variables.data_dir+os.sep+"telecom.bib"

bibli = PDFdl.openBibLib(bibName)

minFreq=3
convertGraph(getdictCoauthors(bibli, minFreq))