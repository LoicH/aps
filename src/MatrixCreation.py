import numpy as np



def fusion_words(list_dic_freq) : # needs dictionnary list. One dictionnary[word : frequency] per document
    list_words=[];                # return all different worlds in all documents
    for dic in list_dic_freq :
        for word in dic :
            if word not in list_words :
                list_words.append(word);
    return list_words

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
    
    
def create_matrix(linkWordDocFreq, list_titles) :
    matrix = np.zeros((len(linkWordDocFreq),len(list_titles)),float) # matrix initialization : words in ligns, columns in lines
    i = 0
    j = 0
    linkWordLine = dict()
    linkDocColumn = dict()
    for title in list_titles :
        linkDocColumn[title]=i
        i=i+1
    for word in linkWordDocFreq :
        linkWordLine[word]=j
        j=j+1
    
    for word in linkWordDocFreq:
        for title in linkWordDocFreq[word]:            
            matrix[linkWordLine[word]][linkDocColumn[title]]=compute_tfidf(linkWordDocFreq,word,title, list_titles)

    return matrix, linkWordLine, linkDocColumn
    
def accessMatrix(matrix, i, j) :
    return matrix[i][j]


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
    
def accessMatrix2(matrix, i, j) :
    for k in range(len(matrix[1])) :
        if matrix[1][k] == i :
            if matrix[2][k] == j :
                return matrix[0][k]
    return 0


def accessMatrix2(matrix, i, j) :
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

u = create_matrix(dic, list_titles)
m=u[0]
n = create_matrix2(dic, list_titles)


t0 = time.clock()
for i in range(len(m)):
    for j in range(len(m[0])) :
        print(accessMatrix(m,i,j))
print("La premiere methode met en secondes :")
print time.clock() - t0

t0 = time.clock()
for i in range(len(m)):
    for j in range(len(m[0])) :
        print(accessMatrix2(n,i,j))
print("La deuxieme methode met en secondes :")
print time.clock() - t0







        
        
