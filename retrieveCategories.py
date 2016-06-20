# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 16:24:43 2016

@author: asueur
"""

import spotlight
from SPARQLWrapper import SPARQLWrapper, JSON

#test <http://dbpedia.org/page/Computer_science>

def getURIs(text): #returns all the URIs linked to words or word groups in the text
    L=[]
    annotations = spotlight.annotate('http://spotlight.sztaki.hu:2222/rest/annotate',text,confidence=0.4, support=20, spotter='Default')
    for i in annotations:
        a=i["URI"]
        L.append(a.encode("UTF-8"))
    return L
#problem to solve : one URI missing when duplicated
                          


    
def getCategories(URIList): #returns all the categories linked to an URL list. Produces duplicates on purpose
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
            L.append(result["label"]["value"].encode("UTF-8").split("/")[-1].replace("_"," ").replace("Category:",""))
    return L
    
def categoryFrequency(categoryList): #returns relative frequency of a category
    n=len(categoryList)
    freq = dict()
    for i in categoryList :
        if i in freq.keys():
            freq[i]=freq[i]+1/float(n)
        else:
            freq[i]=1/float(n)
    return freq
    
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
    return L
#needs testing