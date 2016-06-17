import numpy as np


def fusion_words(list_dic_freq) :
    list_words=[];
    for dic in list_dic_freq :
        for word in dic :
            if word not in list_words :
                list_words.append(word);
    return list_words

def compute_idf(list_dic_freq, word) :
    S = 0;
    for dic in list_dic_freq :
        if dic(word) != 0 :
            S = S+1
    return np.log(len(list_dic_freq)/S)
        
        
def compute_tfidf(list_dic_freq,word, doc) :
    idf = compute_idf(list_dic_freq, word)
    dic = list_dic_freq[doc]
    tf = dic(word)
    tfidf= tf*np.log(idf)
    return tfidf
    
def dic_tfidf_doc_occurence(list_dic_freq, list_words, list_titles) :
    dict_origin_words = dict()
    dict_pdf_occur = dict()
    list_inf_word = []
    list_pdf=[]
    list_occur_pdf = []
    S = 0
    for word in list_words :
        for i in range(len(list_dic_freq)) :
            if word in list_dic_freq[i] :
                list_pdf.append(i)
                list_occur_pdf.append(list_dic_freq(word))
        list_inf_word = [compute_tfidf(list_dic_freq,word)]
    