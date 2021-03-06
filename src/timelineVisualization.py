# -*- coding: utf-8 -*-
"""
Module used to view the timeline.
"""
import PDFdl
import bibtexparser
import re


 



def getAll(index, bibName):
    """returns the information about an article at a given position in a bibtex file
    
    >>> getAll(3, "telecom.bib")
    {u'author': u'S. {Durand} and J. P. {Bello} and B. {DAVID} and G. {Richard}',
     u'title': u'Feature Adapted Convolutional Neural Networks for Downbeat Tracking',
     u'year': u'2016'}
     
     
    @param index: the position of the article in the corpus
    @type index: int
    
    @param bibName: the path leading to the bibtex file
    @type bibName: string
    
    @return: a dictionary of the information about the article, all the strings are in unicode
    @rtype: dict {unicode: unicode}
    
    
    """
    entries=PDFdl.openBibLib(bibName).entries #all the articles
    return bibtexparser.customization.convert_to_unicode(entries[index]) 

def getInfo(authorName, bibName): 
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
    
    @param bibName: the path leading to the bibtex file
    @type bibName: string
    
    @return: the publications informations and the colleagues of a given author
    @rtype: tuple (dict {title (unicode): [date (unicode), ID (int)]}, 
    unicode list)
    

    """
    #datesAndIds : {pubName:[date,id]}
    datesAndIds = dict()
    coauthors=[]
    entries=PDFdl.openBibLib(bibName).entries
    
    for i in entries:
        if authorName.replace(" ","") in i["author"].replace(" ","").replace("{","").replace("}",""):
            try:
                datesAndIds[i["title"]]=[i["year"]+" " + i["month"],int(re.findall(r'id=(\d+)',i["annote"])[0])] #dictionary pubName: [date,id]
            except KeyError:
                print "no month available for document"
            for k in i["author"].replace(" ","").replace("{","").replace("}","").split(" and "):
                if k not in coauthors:
                    coauthors.append(k.replace('}','').replace('{','').replace(" ",""))        
    coauthors=[i for i in coauthors if i!=authorName]     
    return datesAndIds, coauthors

def getCoauthors(authorName, minFreq, biblib): 
    u"""returns the colleagues of a given author if they have enough co-publications
    
        >>> getCoauthors(u'Mazé', 5, "data/telecom.bib")
        [u'E. Nassor', u'F. Denoual', u'F. Maz\xe9', u'C. Concolato', u'J. Le Feuvre']
    
    @param authorName: the last name of an author
    @type authorName: unicode
    
    @param minFreq: the min number of co-publications
    @type minFreq: int
    
    @param biblib: the bib database containing information
    @type biblib: BibDatabase
    
    @return: a list of all the colleagues
    @rtype: unicode list
    
   
"""
    coauthors=[]
    entries=biblib.entries

    for i in entries:
        if authorName.replace(" ","") in i["author"].replace(" ","").replace("{","").replace("}",""):
            for k in i["author"].replace("{","").replace("}","").split(" and "):
                a=k.replace('}','').replace('{','')
                if a.replace(" ","")!="":
                    coauthors.append(k.replace('}','').replace('{',''))        
    coauthors=[i for i in coauthors if i!=authorName]     
    coauthorsFreq = {a:coauthors.count(a) for a in coauthors}    
    coauthors2=[i for i in coauthorsFreq if coauthorsFreq[i]>minFreq]
    return coauthors2