# -*- coding: utf-8 -*-
"""
Module used to retrieve informations and concepts linked to a given text 
using DBpedia Spotlight & SPARQLWrapper
"""

import spotlight
from SPARQLWrapper import SPARQLWrapper, JSON
import os 

app_path = os.getcwd().split(os.sep+"aps")[0]+os.sep+"aps"
data = app_path+os.sep+"data"

def getURIs(text): 
    """returns all the URIs linked to words or word groups in the text
    @param text: text you want to get URIs from
    @type text: string
    
    @return: all URIs DBpedia found linked to the words in text and all words 
    that dbpedia found URIs linked to
    @rtype: tuple (string list, string list)
    
    @warning: spotlight.annotate() doesn't seem to work for lots of texts."""

    
    URIList=[]
    annotatedWords=[]
    annotations = spotlight.annotate('http://spotlight.sztaki.hu:2222/rest/annotate',text,confidence=0.4, support=20, spotter='Default')
    for i in annotations:
        a=i["URI"]
        URIList.append(a.encode("UTF-8"))
        try:
            annotatedWords.append(i["surfaceForm"].encode("utf-8"))
        except AttributeError as e:
            print 'Error adding this word: "%s" (%s)'% (i["surfaceForm"], e.message)
    return URIList, annotatedWords
                          


    
def getCategories(URIList, annotatedWords):
    """returns all the categories linked to an URL list. Produces duplicates on purpose
    
    @param URIList: URIs you want the categories linked to
    @type URIList: string list
    
    @param annotatedWords: words that are linked to each URIs in the URIlist
    @type annotatedWords: string list
    
    @return: list of all categories found with duplicates and match each 
    Category to the words linked to
    @rtype: tuple (string list, dict {string: string list})"""
    
    L=[]
    wordByCategory=dict()
    i=0
    for URI in URIList:
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setQuery("""
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX dc: <http://purl.org/dc/terms/>
            SELECT ?label
            WHERE { """+ "<"+ URI + "> dc:subject ?label }"
        )
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        for result in results["results"]["bindings"]:
            category=result["label"]["value"].encode("UTF-8").split("/")[-1].replace("_"," ").replace("Category:","")
            L.append(category)
            if category in wordByCategory:
                wordByCategory[category].append(annotatedWords[i])
            else:
                wordByCategory[category]=[annotatedWords[i]]
        i+=1
    return L, wordByCategory
    
def categoryFrequency(categoryList):   #TODO delete units
    """returns relative frequency of the 20 most prominent categories
    @param categoryList: raw categories list (with duplicates)
    @type categoryList: string list
    
    @return: match each Categories to its frequency
    @rtype: dict {category (string): frequency (float)}"""
    n=len(categoryList)
    freq = dict()
    for i in categoryList:
        if i in freq.keys():
            freq[i]=freq[i]+1/float(n)
        else:
            freq[i]=1/float(n)
    sortedFreq=sorted([(v,k) for (k,v) in freq.items()], reverse = True)[:10]
    freq=dict([(k,v) for (v,k) in sortedFreq])
    return freq
    
#def textToCatFreq(text):
#    """returns dict{category: frequency } for each category found in the text"""
#    URIs = getURIs(text)
#    return categoryFrequency(getCategories(URIs[0], URIs[1]))
    
#def getWordsLinkedTo(category,URIList): #returns text words linked to a certain category
#    L=[]
#    for URI in URIList:
#        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
#        sparql.setQuery("""
#            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#            PREFIX dc: <http://purl.org/dc/terms/>
#            SELECT ?label
#            WHERE { """+ "<"+ URI + "> dc:subject ?label }"
#        )
#        sparql.setReturnFormat(JSON)
#        results = sparql.query().convert()
#        for result in results["results"]["bindings"]:
#            if result["label"]["value"].encode("UTF-8").split("/")[-1].replace("_"," ").replace("Category:","")== category:
#                L.append(URI.split("/")[-1].replace("_"," ")) 
#    return list(set(L))


def getAll(text): 
    """returns relative frequency of a category, and words linked to categories
    
    @param text: text you want to get category frequency from
    @type text: string    
    
    @return: link categories to their frequencies and match each Categories to the words linked to
    @rtype: tuple(dict{category (string): frequency (float)}, dict{category (string): list word (string list)})"""
    URIs = getURIs(text)
    categories=getCategories(URIs[0], URIs[1] )
    return categoryFrequency(categories[0]),categories[1]
    
