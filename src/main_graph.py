# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 21:35:31 2016

@author: asueur
"""

from graphVisualization import getdictCoauthors
from formatConversion import convertGraph

convertGraph(getdictCoauthors("testbib.bib"))