# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 17:33:59 2016

@author: loic
"""
import os
app_path = os.getcwd().split(os.sep+"aps")[0]+os.sep+"aps"
data = app_path+os.sep+"data"
src = app_path+os.sep+"src"
js = app_path+os.sep+"js"
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello world!"
    
@app.route('/wordcloud')
def wordcloud():
    return render_template('WordCloud.html')    
    #return '<script type="text/javascript" src="'+data+os.sep+'WordCloud.js"></script>'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')