# -*- coding: utf-8 -*-
"""
Module used essentially for formatting dates from "2012 dec" to "2012 12" 
"""
import re
import retrieveCategories

regex = r"(\d+) ([a-zA-Z]+)"

            
def formatMonth(string):
    """ converts from number to month"""
    switcher = { "jan": "01","feb": "02", "mar": "03", "apr": "04","may": "05", "jun": "06", "jul": "07", "aug": "08", "sep": "09", "oct": "10", "nov": "11", "dec": "12" }      
    return switcher.get(string)
    
def formatDate(string): 
    """turns "2015 feb" into "2015 02" for instance"""
    if re.search(regex, string):        # return 0 if the string doesn't match
        match = re.search(r"(\d+) ([a-zA-Z]+)", string)
        date = match.group(0)
        month = match.group(2)
        return date.replace(month, formatMonth(month))
    else:
        print "The date is wrongly formatted, can't convert it."
        return 0

#def formatAllDates(dicDocs): 
#    """format date for each value in the dic
#    
#    @param dicDocs: a dictionary linking docs to a date in the "2015 feb" forma
#    @type dicDocs: dict {[type foo]: string}
#    
#    @return: the same dictionary with date well formatted
#    @rtype: dict {[same type foo]: string}"""
#    
#    for doc, date in dicDocs.items():      # dic{doc: date}
#        dicDocs[doc] = formatDate(date)

#def chronologicalOrder(dicDocs):
#    """sort docs by chronological order
#    @param dicDocs: a dictionary with docs and dates
#    @type dicDocs: dict {docname (type foo): date (string)}
#    
#    @return: the sorted list of """
#    sortedDocs= sorted([(k,v) for (k,v) in dicDocs.items()])
#    return sortedDocs
#
#def categoriesDoc(listDocs, dicTitleText): # listDocs is a list of docs from an author ordered by chronological order
#    listCategoriesDocs = []                 # dicTitleText links title of a doc to their text
#    for doc in listDocs:                   # returns a list. Each element contains the a dictionnary[category: frequency] for each doc
#        listCategoriesDocs.append(retrieveCategories.textToCatFreq(dicTitleText(doc)))
#    return listCategoriesDocs
#    
#def allCategories(listCategoriesDocs): # get all categories from all the docs
#    listAllCategories = []
#    for doc in listCategoriesDocs:
#        for category in doc:
#            if category not in listAllCategories:
#                listAllCategories.append(category)
#    return listAllCategories



