# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 11:55:20 2016

@author: alagasse
"""
import re
import sys
import retrieveCategories
import MatrixCreation

regex = r"(\d+) ([a-zA-Z]+)"

def selecDocsByAuthor(listDocs, author) : #  select the docs written by an author
    l = []
    for doc in listDocs :
        if doc.author == author :
            l.append(doc)
            
def stringToNumber(string): # turn month from string to number
    switcher = { "jan" : 1,"feb": 2, "mar": 3, "apr" : 4,"may" : 5, "jun" : 6, "jul" : 7, "aug" : 8, "sep" : 9, "oct" : 10, "nov" : 11, "dec" : 12 }      
    return switcher.get(string)
    
def stringToTuple(string) : # turn string "Year Month(string)" to tuple ("Year", Month(number))
    if re.search(regex, "2016 dec"):
        match = re.search(regex, "2016 dec")
        return (match.group(1), match.group(2))
    else:
        sys.exist()
    
def chronologicalOrder(listDocs) : # sort docs by chronological order
    l=sorted(listDocs, key=stringToTuple(attrgetter("date")))
    return l
   
### test regular expression
if re.search(regex, "2016 dec"):
    # Indeed, the expression "([a-zA-Z]+) (\d+)" matches the date string
    
    # If we want, we can use the MatchObject's start() and end() methods 
    # to retrieve where the pattern matches in the input string, and the 
    # group() method to get all the matches and captured groups.
    match = re.search(regex, "2016 dec")
    
    # This will print [0, 7), since it matches at the beginning and end of the 
    # string
    print "Match at index %s, %s" % (match.start(), match.end())
    
    # The groups contain the matched values.  In particular:
    #    match.group(0) always returns the fully matched string
    #    match.group(1) match.group(2), ... will return the capture
    #            groups in order from left to right in the input string
    #    match.group() is equivalent to match.group(0)
    
    # So this will print "June 24"
    print "Full match: %s" % (match.group(0))
    # So this will print "June"
    print "Year: %s" % (match.group(1))
    # So this will print "24"
    print "Month: %s" % (match.group(2))
else:
    # If re.search() does not match, then None is returned
    print "The regex pattern does not match. :("


def categoriesDoc(listDocs, dicTitleText) : # listDocs is a list of docs from an author ordered by chronological order
    listCategoriesDocs = []                 # dicTitleText links title of a doc to their text
    for doc in listDocs :                   # returns a list. Each element contains the a dictionnary[category : frequency] for each doc
        listCategoriesDocs.append(retrieveCategories.textToCatFreq(dicTitleText(doc)))
    return listCategoriesDocs
    

    
    
def importantCategories(listCategoriesDocs, numberCategories) :
    d = dict()
    for dic in listCategoriesDocs :
        for category in dic :
            if category not in d :
                d[category] = dic[category]
            else :
                d[category] = d[category] + dic[category]
    return d






