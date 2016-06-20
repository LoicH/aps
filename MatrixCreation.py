import numpy as np


def fusion_words(list_dic_freq) : # needs dictionnary list. One dictionnary[word : frequency] per document
    list_words=[];                # return all different worlds in all documents
    for dic in list_dic_freq :
        for word in dic :
            if word not in list_words :
                list_words.append(word);
    return list_words

#def compute_idf(list_dic_freq, word) :
#    S = 0;
#    for dic in list_dic_freq :
#        if dic(word) != 0 :
#            S = S+1
#    return np.log(len(list_dic_freq)/S)
        
        
#def compute_tfidf(list_dic_freq,word, doc) :
#    idf = compute_idf(list_dic_freq, word)
#    dic = list_dic_freq[doc]
#    tf = dic(word)
#    tfidf= tf*np.log(idf)
#    return tfidf

def linkWordDocFreq(list_dic_freq, list_titles) : # needs : - dictionnary list. One dictionnary[word : frequency] per document. 
                                                  #         - titles list 
    dict_origin_words = dict()                    # returns one dictionnary[word : dictionnary : [ doc where this word is : word frequency in this doc]]
    dict_pdf_occur = dict()                       # To put it simply, for each world we have access to his frequency in each doc where the word is.
    list_words = fusion_words (list_dic_freq)
    for word in list_words :
        dict_pdf_occur = dict()
        for i in range(len(list_dic_freq)) :
            if word in list_dic_freq[i] :
                dict_pdf_occur[list_titles[i]]=list_dic_freq[i][word]
        dict_origin_words[word]=dict_pdf_occur
    return dict_origin_words


def compute_tfidf(linkWordDocFreq, word, title, list_titles) : # computes tfidf from the dictionnary which associates words and their frequencies in each document
    if title in linkWordDocFreq[word] :
        tf = linkWordDocFreq[word][title]
    else :          # if the word in not in this doc : tf = 0 --> tfidf = 0
        return 0
    idf= float(len(list_titles))/len(linkWordDocFreq[word])
    return tf*np.log(idf)
    
#def create_matrix(dic_mot_doc_occurence, list_titles) :
#    list_not_null_values = []
#    list_columns = []
#    list_lines = []
#    list_words = []
#    i = 0
#    tfidf = 0
#    for word in dic_mot_doc_occurence :
#        for j in range(len(list_titles)) :
#            title = list_titles[j]
#            tfidf = compute_tfidf2(dic_mot_doc_occurence, word, title, list_titles)
#            if tfidf != 0 :
#                list_not_null_values.append(tfidf)
#                list_columns.append(i)
#                list_words.append(word)
#                list_lines.append(j)
#        i=i+1
#    return [list_not_null_values, list_columns, list_words, list_lines]
    
#def create_matrix2(dic_mot_doc_occurence, list_titles) :
#    list_not_null_values = []
#    dic_columns = dict()
#    dic_lines = dict()
#    i = 0
#    tfidf = 0
#    for word in dic_mot_doc_occurence :
#        for j in range(len(list_titles)) :
#            title = list_titles[j]
#            tfidf = compute_tfidf2(dic_mot_doc_occurence, word, title, list_titles)
#            if tfidf != 0 :
#                list_not_null_values.append(tfidf)
#                dic_columns[i] = word
#                dic_lines[j] = title
#        i=i+1
#    return [list_not_null_values, dic_columns, dic_lines]
    
def create_matrix(linkWordDocFreq, list_titles) :
    matrix = np.zeros((len(list_titles),len(linkWordDocFreq)),float) # matrix initialization : words in columns, documents in lines
    i = 0
    j = 0
    linkDocLine = dict()
    linkWordColumn = dict()
    for title in list_titles :
        linkDocLine[title]=i
        i=i+1
    for word in linkWordDocFreq :
        linkWordColumn[word]=j
        j=j+1
    
    for word in linkWordDocFreq:
        for title in linkWordDocFreq[word]:            
            matrix[linkDocLine[title]][linkWordColumn[word]]=compute_tfidf(linkWordDocFreq,word,title, list_titles)

    return matrix, linkDocLine, linkWordColumn
    
def index2(list, i) :
    pos = []
    j = 0
    for a in list :
        if a == i :
            pos.append(j)
        j+=1
    return pos

def create_matrix2(linkWordDocFreq, list_titles) :
    listNonNullValues = []
    listLines = []
    listColumns = []
    i = 0
    j = 0
    linkDocLine = dict()
    linkWordColumn = dict()
    
    for title in list_titles :
        linkDocLine[title]=i
        i=i+1
    for word in linkWordDocFreq :
        linkWordColumn[word]=j
        j=j+1
    
    for word in linkWordDocFreq:
        for title in linkWordDocFreq[word]:   
            tfidf = compute_tfidf(linkWordDocFreq,word,title, list_titles)
            if tfidf != 0 :
                listNonNullValues.append(tfidf)
                listLines.append(linkDocLine[title])
                listColumns.append(linkWordColumn[word])

    return listNonNullValues, listLines, listColumns, linkDocLine, linkWordColumn
    
def accessMatrix(matrix, i, j) :
    for k in range(len(matrix[1])) :
        if matrix[1][k] == i :
            if matrix[2][k] == j :
                return matrix[0][k]
    return 0

    
dic_freq1 = dict()
dic_freq2 = dict()
dic_freq3 = dict()

dic_freq1["poisson"] = 0.5
dic_freq1["a"]=0.4
dic_freq1["b"]=0.6

dic_freq2["viande"] = 0.6
dic_freq2["a"]=0.7
dic_freq2["b"]=0.8

dic_freq3["oeuf"] = 0.4
dic_freq3["a"]=0.7
dic_freq3["c"]=0.2

list_dic_freq = [dic_freq1, dic_freq2, dic_freq3] 
list_titles= ["ninja", "samourai", "wasabi"]
dic = linkWordDocFreq(list_dic_freq, list_titles)