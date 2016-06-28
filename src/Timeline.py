# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 11:55:20 2016

@author: alagasse
"""
import re
import sys
import retrieveCategories
import TFIDFMatrixClass
import freqMatrixClass

regex = r"(\d+) ([a-zA-Z]+)"

def selecDocsByAuthor(listDocs, author): 
    """select the docs written by an author
    @param listDocs: all docs in a corpus
    @type listDocs: doc list
    
    @param author: author name
    @type author: string
    
    @return: all docs written by the author in the corpus
    @rtype: doc list"""
    l = []
    for doc in listDocs:
        if doc.author == author:
            l.append(doc)
            
def formatMonth(string): # turn month from string to number
    switcher = { "jan": "01","feb": "02", "mar": "03", "apr": "04","may": "05", "jun": "06", "jul": "07", "aug": "08", "sep": "09", "oct": "10", "nov": "11", "dec": "12" }      
    return switcher.get(string)
    
def formatDate(string): 
    """turn "2015 feb" in "2015 02" for instance"""
    if re.search(regex, string):        # return 0 if the string doesn't match
        match = re.search(r"(\d+) ([a-zA-Z]+)", string)
        date = match.group(0)
        month = match.group(2)
        return date.replace(month, formatMonth(month))
    else:
        print "The regex pattern does not match.:("
        return 0

def formatAllDates(dicDocs): # format date for each value in the dic of all docs written by an author
    for doc in dicDocs:      # dic{doc: date}
        dicDocs[doc] = formatDate(dicDocs[doc])

def chronologicalOrder(listDocs): # sort docs by chronological order
    sortedDocs= sorted([(k,v) for (k,v) in listDocs.items()])
    return sortedDocs
   
### test regular expression
#if re.search(regex, "2016 dec"):
#    # Indeed, the expression "([a-zA-Z]+) (\d+)" matches the date string
#    
#    # If we want, we can use the MatchObject's start() and end() methods 
#    # to retrieve where the pattern matches in the input string, and the 
#    # group() method to get all the matches and captured groups.
#    match = re.search(regex, "2016 dec")
#    
#    # This will print [0, 7), since it matches at the beginning and end of the 
#    # string
#    print "Match at index %s, %s" % (match.start(), match.end())
#    
#    # The groups contain the matched values.  In particular:
#    #    match.group(0) always returns the fully matched string
#    #    match.group(1) match.group(2), ... will return the capture
#    #            groups in order from left to right in the input string
#    #    match.group() is equivalent to match.group(0)
#    
#    # So this will print "June 24"
#    print "Full match: %s" % (match.group(0))
#    # So this will print "June"
#    print "Year: %s" % (match.group(1))
#    # So this will print "24"
#    print "Month: %s" % (match.group(2))
#else:
#    # If re.search() does not match, then None is returned
#    print "The regex pattern does not match.:("


def categoriesDoc(listDocs, dicTitleText): # listDocs is a list of docs from an author ordered by chronological order
    listCategoriesDocs = []                 # dicTitleText links title of a doc to their text
    for doc in listDocs:                   # returns a list. Each element contains the a dictionnary[category: frequency] for each doc
        listCategoriesDocs.append(retrieveCategories.textToCatFreq(dicTitleText(doc)))
    return listCategoriesDocs
    
def allCategories(listCategoriesDocs): # get all categories from all the docs
    listAllCategories = []
    for doc in listCategoriesDocs:
        for category in doc:
            if category not in listAllCategories:
                listAllCategories.append(category)
    return listAllCategories



