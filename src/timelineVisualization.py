# -*- coding: utf-8 -*-
"""
Module used to view the timeline.
"""
import PDFdl
import bibtexparser
import re
import os

app_path = os.getcwd().split(os.sep+"aps")[0]+os.sep+"aps"
data = app_path+os.sep+"data"
src = app_path+os.sep+"src"

regex=r'id=(\d+)' 
bib = data+os.sep+'document.bib'  ### bib name (can be modified)
entries=PDFdl.openBibLib(bib).entries  #all of the bib's articles


def getAll(index,bibName):
    """returns the information about an article at a given position in a bibtex file
    
    >>> getAll(3, "toto")
    {u'author': u'S. {Durand} and J. P. {Bello} and B. {DAVID} and G. {Richard}',
     u'title': u'Feature Adapted Convolutional Neural Networks for Downbeat Tracking',
     u'year': u'2016'}
     
     
    @param index: the position of the article in the corpus
    @type index: int
    
    @param bibName: the path leading to the bibtex file (useless)
    @type bibName: string
    
    @return: a dictionary of the information about the article, all the strings are in unicode
    @rtype: dict {unicode: unicode}
    
    
    """
    return bibtexparser.customization.convert_to_unicode(entries[index]) 

def getInfo(authorName): 
    u"""returns the publication and colleagues of a given author 
    
        >>> pub, colleagues = getInfo(u"Clémençon")
        >>> pub
        {u'Multipartite Ranking': [u'2014 jul',
        14057],
        u'Visual Mining of Epidemic Networks': [u'2011 jun', 11289]}
        >>> colleagues
        [u'S.Cl\xe9men\xe7onandH.DeArazozaandV.Ch.TranandF.Rossi',
        u'R.GaudelandS.Cl\xe9men\xe7on']   
        
    @param authorName: the last name of the author        
    @type authorName: unicode
    
    @return: the publications informations and the colleagues of a given author
    @rtype: tuple (dict {title (unicode): [date (unicode), ID (int)]}, 
    unicode list)
    

    """
    #datesAndIds : {pubName:[date,id]}
    datesAndIds = dict()
    coauthors=[]
    for i in entries:
        if authorName.replace(" ","") in i["author"].replace(" ","").replace("{","").replace("}",""):
            try:
                datesAndIds[i["title"]]=[i["year"]+" " + i["month"],int(re.findall(regex,i["annote"])[0])] #dictionnary pubName: [date,id]
            except KeyError:
                print "no month available for document"
            for k in i["author"].replace(" ","").replace("{","").replace("}","").split(" and "):
                if k not in coauthors:
                    coauthors.append(k.replace('}','').replace('{','').replace(" ",""))        
    coauthors=[i for i in coauthors if i!=authorName]     
    return datesAndIds, coauthors

def getCoauthors(authorName):
    u"""returns the colleagues of a given author.
    
        >>> getCoauthors(u'Mazé')
        [u'E. Nassor', u'F. Denoual', u'F. Maz\xe9', u'C. Concolato', u'J. Le Feuvre']
    
    @param authorName: the last name of an author
    @type authorName: unicode
    
    @return: a list of all the colleagues
    @rtype: unicode list
    
   
"""
    coauthors=[]
    for i in entries:
        if authorName.replace(" ","") in i["author"].replace(" ","").replace("{","").replace("}",""):
            for k in i["author"].replace("{","").replace("}","").split(" and "):
                a=k.replace('}','').replace('{','')
                if a.replace(" ","")!="":
                    coauthors.append(k.replace('}','').replace('{',''))        
    coauthors=[i for i in coauthors if i!=authorName]     
    coauthorsFreq = {a:coauthors.count(a) for a in coauthors}    
    coauthors2=[i for i in coauthorsFreq if coauthorsFreq[i]>10]
    return coauthors2