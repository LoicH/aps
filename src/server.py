# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 17:33:59 2016

@author: loic
"""

from flask import Flask, render_template
import threading
import initServer
import os

app_path = os.getcwd().split(os.sep+"aps")[0]+os.sep+"aps"
data = app_path+os.sep+"data"
src = app_path+os.sep+"src"
"""Directing the routes"""
app = Flask(__name__)

print "In server.py, __name__ =",__name__
@app.route('/')
def index():
    return render_template('index.html')    
    
@app.route('/wordcloud/')
def wordcloud():
    return render_template('wordcloud.html') 
    
@app.route('/timeline/')
def timeline():
    return render_template('timeline.html') 
    
@app.route('/testjs/')
def testjs():
    return render_template('testjs.html')  
    
@app.route('/author/<name>')
def show_author(name):
    print "Name:",name
    return render_template('author.html', name=name)

@app.route('/init_wordcloud/')
def init_wordcloud():
    threading.Thread(initServer.make_json_wordcloud2(data+os.sep+"concolato.bib"))
    return "Word Cloud done"





if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', threaded=True)