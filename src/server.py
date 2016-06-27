# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 17:33:59 2016

@author: loic
"""
import os
app_path = os.getcwd().split(os.sep+"aps")[0]+os.sep+"aps"
data = app_path+os.sep+"data"
src = app_path+os.sep+"src"
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')    
    
@app.route('/wordcloud/')
def wordcloud():
    return render_template('WordCloud.html')    
    
@app.route('/testjs/')
def testjs():
    return render_template('testjs.html')  
    
@app.route('/author/<name>')
def show_author(name):
    return "Welcome to the overview of <b> %s" % name

if __name__ == "__main__":
    print "Server running in",os.getcwd()
    app.run(debug=True, host='0.0.0.0')
    