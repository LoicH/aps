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
    
def dic_mot_doc_occurence(list_dic_freq, list_titles) :
    dict_origin_words = dict()
    dict_pdf_occur = dict()
    list_words = fusion_words (list_dic_freq)
    for word in list_words :
        dict_pdf_occur = dict()
        for i in range(len(list_dic_freq)) :
            if word in list_dic_freq[i] :
                dict_pdf_occur[list_titles[i]]=list_dic_freq[i][word]
        dict_origin_words[word]=dict_pdf_occur
    return dict_origin_words


def compute_tfidf2(dic_mot_doc_occurence, word, title, list_titles) :
    tf = dic_mot_doc_occurence[word][title]
    idf= len(list_titles)/len(dic_mot_doc_occurence[word])
    return tf*np.log(idf)
    
def create_matrix(dic_mot_doc_occurence, list_titles) :
    list_not_null_values =[]
    list_
    





dic_freq1 = dict()
dic_freq2 = dict()
dic_freq1["poisson"] = 0.5
dic_freq1["a"]=0.4
dic_freq1["b"]=0.6
dic_freq2["viande"] = 0.5
dic_freq2["a"]=0.7
dic_freq2["b"]=0.8
list_dic_freq = [dic_freq1, dic_freq2] 
list_titles= ["ninja", "samourai"]
dic = dic_mot_doc_occurence(list_dic_freq, list_titles)