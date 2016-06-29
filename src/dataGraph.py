# -*- coding: utf-8 -*-
"""
Performs computations for the graph visualization, like timelineVisualization
"""

import PDFdl
import timelineVisualization
    
def distanceTFIDF(A,B):
    """ return a number related to the similarity between matrixes
    @param A : TFIDF matrix to compare
    @type A : TFIDFMatrix
    
    @param B : TFIDF matrix to compare
    @type B : TFIDFMatrix
                             
    @return: similarity coefficient
    @rtype: float  
    """
    a=A.sum_words()
    b=B.sum_words()
    for word in b:
        if word not in a:
            a[word]=0
    for word in a:
        if word not in b:
            b[word]=0
    scal=0
    for i in a:
        scal+=a[i]*b[i]
    return scal
       

def getAllAuthors(bibli): 
    """ return a list with all the authors in the bib

    
    @param bibli: the file containing the information about authors
    @type bibli: bibDatabase
                             
    @return: all authors from the bib
    @rtype: string list """
    authorList=[]

    for article in bibli.entries:
        authors=article["author"].replace("{","").replace("}","").split(" and ")
        for author in authors:
            if author not in authorList:
                authorList.append(author)
    return authorList
    
def getdictCoauthors(bibName, minFreq):
    """ return a list with all the coauthors in the bib
    @param bibName: the path to the bib you want to get the coauthors from
    @type bibName: string
    
    @param minFreq: the minimum of publications authors must have in common
    @type minFreq: int
                             
    @return: all coauthors from the bib linked to the authors
    @rtype: dictionary {author (string): list coauthors (string list)} """
    authorList=getAllAuthors(bibName)
    n=len(authorList)
    dictCoauthors=dict()
    i=0
    for author in authorList:
        print "(%d/%d)"% (i+1, n)
        if author!='':
            print "getdictCoauthors is computing",author
            coauthors=timelineVisualization.getCoauthors(author, minFreq, bibName)
            if coauthors!=[]:
                dictCoauthors[unicode(author)]=coauthors
        i+=1
        if i%100==0:
            print str(int(100*float(i)/n)) + "% completed"
    for i in dictCoauthors.values():
        for k in i:
            if k not in dictCoauthors.keys():
                dictCoauthors[k]=[]
    return dictCoauthors
    
