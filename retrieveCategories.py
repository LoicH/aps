# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 16:24:43 2016

@author: asueur
"""

import spotlight
from SPARQLWrapper import SPARQLWrapper, JSON


def getURIs(text): 
    L=[]
    annotations = spotlight.annotate('http://spotlight.sztaki.hu:2222/rest/annotate',text,confidence=0.4, support=20, spotter='Default')
    for i in annotations:
        a=i["URI"]
        L.append(a.encode("UTF-8"))
    return L
#problem to solve : one URI missing when duplicated
                          


    
def getCategories(URIList):
    L=[]
    for URI in URIList:
        URI="<http://dbpedia.org/page/Computer_science>"
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setQuery("""
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?label
            WHERE { """+ URI + " dc:subject ?label }"
        )
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        for result in results["results"]["bindings"]:
            print(result["label"]["value"])
            L.append(result["label"]["value"])
    return L
    
#to test