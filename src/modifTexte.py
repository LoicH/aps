# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 16:42:50 2016

@author: asueur
"""





# blackList: banned words list
import string
import nltk
from nltk.corpus import wordnet



#tests
#if __name__ == "__main__":
    
    #pdfPath = "/cal/homes/asueur/Downloads/TP3.pdf"
    #text1 = "abc Abc bAc.... bBc bacb acb acb acb and ant ham"
    #randomText="""Still court no small think death so an wrote. Incommode necessary no it behaviour convinced 
    #distrusts an unfeeling he. Could death since do we hoped is in. Exquisite no my attention extensive. 
    #The determine conveying moonlight age. Avoid for see marry sorry child. Sitting so totally 
    #forbade hundred to.Their could can widen ten she any. As so we smart those money in. Am wrote up whole 
    #so tears sense oh. Absolute required of reserved in offering no. How sense found our those gay again 
    #taken the. Had mrs outweigh desirous sex overcame. Improved property reserved disposal do offering me"""
    #blackList=["abc","acb"]



def delPunctuation(text):
    """deleting punctuation
    @param text: text you want to delete punctuation 
    @type text: string
    
    @return: text without punctuation
    @rtype: string """
    for char in string.punctuation: 
        text=text.replace(char,'')
    return text.replace('\x0c','')
    
def getTextWords(text):
    """tokenize words
    @param text: text you want to tokenize
    @type text: string
    
    @return: word list
    @rtype: string list """
    return nltk.word_tokenize(text)

def modifyText(textWords, blackList):
    """deleting one letter words + lowercase (except acronyms)
    @param textWords: word list
    @type textWords: string list
    
    @param blackList: words you want to delete in textWords
    @type blacklist: string list
    
    @return: word list without one letter words. All words in lowercase, except acronyms
    @rtype: string list """
    i=0
    for word in textWords:
        if len(word) == 1:
            textWords.remove(word)
            i -= 1
        elif not word.isupper():
            textWords[i]=word.lower()
        i += 1
    for w in blackList:
        textWords = textWords.replace(w,'')
    return textWords
    
def deleteStopWords(textWords):
    """deleting words of types determiners, conjonctions, cardinal numbers and stopwords
    @param text: word list you want to delete stopwords from
    @type text: string list
    
    @return: word list without stopwords, determiners ...
    @rtype: string list """
    listCopy=textWords
    stopwords= nltk.corpus.stopwords.words("english")
    for sw in stopwords:
        listCopy=[j for j in listCopy if j!=str(sw)]
    types = nltk.pos_tag(listCopy)    
    #print types
    for i in types:
        if i[1] in ["DT","CC", "CD", "PRP", "PRP$", "PDT"]:  
            listCopy.remove(i[0])
    return listCopy
    
#def lemmatization(textWords): basic lemmatizer
#    #lemmatizes all the words
#    words = textWords
#    lmtzr=WordNetLemmatizer()
#    for i in range(len(words)):
#        words[i]=lmtzr.lemmatize(words[i])
#    return words
    

#def compteur(text, wordList):
#    text=delPunctuation(text)
#    dictionnary={}
#    textWords=text.split()
#    for word in wordList:
#        a=0
#        for word2 in textWords:
#            if (word==word2):
#                a+=1
#            dictionnary[word]=str(a/float(len(textWords)))
#    return dictionnary
    

def get_wordnet_pos(treebank_tag): 
    """convert pos_tag from nltk to pos_tag from wordnet
    @param treebank_tag: tag from nltk
    @type treebank_tag: string 
    
    @return: tag from wordnet
    @rtype: string (one letter) """
    if treebank_tag.startswith('J'):
        return "a"
    elif treebank_tag.startswith('V'):
        return "v"
    elif treebank_tag.startswith('N'):
        return "n"
    elif treebank_tag.startswith('R'):
        return "r"
    else:
        return 'n'

def lemmatization(textWords): 
    """lemmatizes all the words
    @param textWords: word list
    @type textWords: string list
    
    @return: lemmatized words
    @rtype: string list """
    words = textWords
    p = nltk.pos_tag(textWords)
    lmtzr=nltk.WordNetLemmatizer()
    for i in range(len(p)):
        words[i]=lmtzr.lemmatize(p[i][0], get_wordnet_pos(p[i][1]))
    return words
        
def frequency(textWords):
    """gives the frequency of each word in the text
    
    @param textWords: word list
    @type textWords: string list
    
    @return: link each word with its frequency in the world list
    @rtype: dict[ word (string): frequency (float) ] """
    a=nltk.FreqDist(textWords)
    nbMots = 0
    for word in a:
        nbMots = nbMots + a[word]
    for i in a.keys():
        a[i]=a[i]/float(nbMots)
    return a

def frequencyWithTreshold(textWords, occTreshold, lengthTreshold):
    """gives the frequency of each word in the text
    
    @param textWords: word list
    @type textWords: string list
    
    @param occTreshold: world with less occurences than occTreshold will be wiped out
    @type occTreshold: int
    
    @param occTreshold: world with less letters than lengthTreshold will be wiped out
    @type occTreshold: int

    @return: world list without the world below the two tresholds
    @rtype: string list """
    a=nltk.FreqDist(textWords)
    nbMots = 0
    wordsToRemove = []
    for word in a:
        if a[word] <= occTreshold or len(word) <= lengthTreshold:
            wordsToRemove.append(word)
        else:
            nbMots = nbMots + a[word]
    for word in wordsToRemove:
        del a[word]
    for i in a.keys():
        a[i]=a[i]/float(nbMots)
    return a

#if __name__ == "__main__":
#    text = word_tokenize("""The aim of a probabilistic logic (also probability logic and probabilistic reasoning) is to combine the capacity of probability theory to handle uncertainty with the capacity of deductive logic to exploit structure of formal argument. The result is a richer and more expressive formalism with a broad range of possible application areas. Probabilistic logics attempt to find a natural extension of traditional logic truth tables: the results they define are derived through probabilistic expressions instead. A difficulty with probabilistic logics is that they tend to multiply the computational complexities of their probabilistic and logical components. Other difficulties include the possibility of counter-intuitive results, such as those of Dempster-Shafer theory. The need to deal with a broad variety of contexts and issues has led to many different proposals.""")
#    w= textToDictionnary(t, [])
#    d = frequency(w)
#    e = frequencyWithTreshold(w, 2, 0)
#    for word in d:
#        if word in e:
#            print(word)
    
def textToDictionnary(text, blackList):
    """does all the functions above in one take"""
    f= frequency(lemmatization(deleteStopWords(modifyText(getTextWords(delPunctuation(text)),blackList))))
    dic = dict()
    for word in f.keys():
        dic[word] = f[word]
    return dic
    
"""Estimating the language of a text"""



def estimate_language(text):
    """returns the most probable language of the text.
     @param text: Text you want the language
     @type text: str
     
     @return: Most probable language guessed
     @rtype: str
     """
    words = [word.lower() for word in nltk.wordpunct_tokenize(text)]
    best_language = ''
    score = 0
    for language in nltk.corpus.stopwords.fileids():
        stopw = nltk.corpus.stopwords.words(language)
        common= set(words).intersection(set(stopw))
#        print language,":",common
        if len(common) > score:
            best_language = language
            score = len(common)
           # print "New best"
    return best_language

if __name__ == "__main__":
    t = """If the score is close to 0 (appearing in black),
this means that the consensus between input clusterings is
very high; it appears in white for unstable data, i.e. data that
are classiﬁed with different neighbors according to the input
clusterings. We observe, consistently with the preceding ob-
servations on clusters, that most pixels are very stable. The
unstable ones seem to be located at the frontier of objects, in
the dark areas of the consensually classiﬁed image. Again,
it would indicate to the interpreters that these pixels (corre-
sponding to the previously mentioned black clusters) deserve"""
    print estimate_language(t)
    
    t = """Albert Einstein (en allemand: [ˈalbɐt ˈaɪnʃtaɪn] Prononciation du titre dans sa version originale Écouter) né le 14 mars 1879 N 1 à Ulm, Wurtemberg, et mort le 18 avril 1955 à Princeton, New Jersey est un physicien théoricien qui fut successivement allemand, apatride (1896), suisse (1901) et sous la double nationalité helvético-américaine (1940)1. Il publie sa théorie de la relativité restreinte en 1905, et sa théorie de la gravitation dite relativité générale en 1915. Il contribue largement au développement de la mécanique quantique et de la cosmologie, et reçoit le prix Nobel de physique de 1921 pour son explication de l’effet photoélectrique2. Son travail est notamment connu du grand public pour l’équation E=mc2, qui établit une équivalence entre la matière et l’énergie d’un système.Il est aujourd'hui considéré comme l'un des plus grands scientifiques de l'histoire, et sa renommée dépasse largement le milieu scientifique. Il est la personnalité du XXe siècle selon l'hebdomadaire Time."""
    print estimate_language(t)
    
    t = u"""Acknowledgements

This work has been partially supported by the Conseil r´egional
d’ˆIle-de-France under a doctoral allowance of its program R´eseau
de Recherche Doctoral en Math´ematiques de l’ˆIle de France
(RDM-IdF) for the period 2012 - 2015 and by the Labex LMH
(ANR-11-IDEX-003-02).

References

[1] Pierre Alquier and Olivier Wintenberger. Model selection
for weakly dependent time series forecasting. Bernoulli,
18(3): 883-913, 2012.

[2] Olivier Catoni and Jean Picard. Statistical Learning The-
ory and Stochastic Optimization: Ecole D’´et´e de Prob-
abilit´es de Saint-Flour XXXI-2001. Number n 1851 in
Ecole d’ ´Et´e de Probabilit´es de Saint-Flour. Springer-
Verlag, 2004.

[3] Krzysztof Łatuszy´nski and Wojciech Niemiro. Rigorous
conﬁdence bounds for MCMC under a geometric drift
condition. J. Complexity, 27(1): 23-38, 2011.

[4] K. L. Mengersen and R. L. Tweedie. Rates of convergence
of the Hastings and Metropolis algorithms. Ann. Statist.,
24(1): 101-121, 1996.

[5] Eric Moulines, Pierre Priouret, and Franc¸ois Roueﬀ. On
recursive estimation for time varying autoregressive pro-
cesses. Ann. Statist., 33(6): 2610-2654, 2005.

[6] Emmanuel Rio. In´egalit´es de Hoeﬀding pour les fonc-
tions lipschitziennes de suites d´ependantes. Comptes
Rendus de l’Acad´emie des Sciences Series I Mathemat-
ics, 330(10):905908, 2000."""

    print textToDictionnary(t, [])