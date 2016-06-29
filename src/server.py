# -*- coding: utf-8 -*-
"""
Module managing the server and redirecting the inputs
"""

import os
from flask import Flask, render_template
import threading
import initServer
import variables 

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
    bib = "concolato.bib"
    threading.Thread(initServer.make_json_wordcloud(
        variables.data_dir+os.sep+bib))
    return "Word Cloud for "+bib+" done"



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', threaded=True)