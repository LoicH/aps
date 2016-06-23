# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 16:24:43 2016

@author: asueur
"""

import spotlight
from SPARQLWrapper import SPARQLWrapper, JSON

#test <http://dbpedia.org/page/Computer_science>

def getURIs(text): #returns all the URIs linked to words or word groups in the text #unknown influence of parameters
    URIList=[]
    annotatedWords=[]
    annotations = spotlight.annotate('http://spotlight.sztaki.hu:2222/rest/annotate',text,confidence=0.4, support=20, spotter='Default')
    for i in annotations:
        a=i["URI"]
        URIList.append(a.encode("UTF-8"))
        annotatedWords.append(str(i["surfaceForm"]))
    return URIList, annotatedWords
                          


    
def getCategories(URIList, annotatedWords): #returns all the categories linked to an URL list. Produces duplicates on purpose
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
    
def categoryFrequency(categoryList): #returns relative frequency of a category
    n=len(categoryList)
    freq = dict()
    for i in categoryList :
        if i in freq.keys():
            freq[i]=freq[i]+1/float(n)
        else:
            freq[i]=1/float(n)
    return freq
    
def textToCatFreq(text) :
    URIs = getURIs(text)
    return categoryFrequency(getCategories(URIs[0], URIs[1]))
    
def getWordsLinkedTo(category,URIList): #returns text words linked to a certain category
    L=[]
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
            if result["label"]["value"].encode("UTF-8").split("/")[-1].replace("_"," ").replace("Category:","")== category:
                L.append(URI.split("/")[-1].replace("_"," ")) 
    return list(set(L))


def getAll(text): #returns relative frequency of a category, and words linked to categories
    categories=getCategories(getURIs(text)[0], getURIs(text)[1] )
    return categoryFrequency(categories[0]),categories[1]
