# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 16:42:50 2016

@author: asueur
"""





# blackList : banned words list
import string
from nltk import *
import os

#tests
pdfPath = "/cal/homes/asueur/Downloads/TP3.pdf"
text1 = "abc Abc bAc.... bBc bacb acb acb acb and ant ham"
randomText="Still court no small think death so an wrote. Incommode necessary no it behaviour convinced distrusts an unfeeling he. Could death since do we hoped is in. Exquisite no my attention extensive. The determine conveying moonlight age. Avoid for see marry sorry child. Sitting so totally forbade hundred to.Their could can widen ten she any. As so we smart those money in. Am wrote up whole so tears sense oh. Absolute required of reserved in offering no. How sense found our those gay again taken the. Had mrs outweigh desirous sex overcame. Improved property reserved disposal do offering me"
blackList=["abc","acb"]


#deleting punctuation
def delPunctuation(text):
    for char in string.punctuation: 
        text=text.replace(char,'')
    return text
    
def getTextWords(text):
    return word_tokenize(text)

#deleting useless words + lowercase
def modifyText(textWords, blackList):
    for i in range(len(textWords)):
        if(textWords[i].islower()):
            textWords[i]=textWords[i].lower()
    for i in blackList :
        textWords = textWords.replace(i,'')
    return textWords
    
    
    
    

    
def deleteStopWords(textWords):
    #deleting words of types determiners, conjonctions, cardinal numbers and stopwords
    listCopy=textWords
    stopwords= corpus.stopwords.words("english")
    for sw in stopwords:
        listCopy=[j for j in listCopy if j!=str(sw)]
    types = pos_tag(listCopy)      
    for i in types:
        if i[1] in ["DT","CC", "CD", "PRP", "PRP$", "PDT"] :  
            listCopy.remove(i[0])
    return listCopy
    
def lemmatization(textWords):
    words = textWords
    lmtzr=WordNetLemmatizer()
    for i in range(len(words)):
        words[i]=str(lmtzr.lemmatize(words[i]))
    return words
    
    
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
    

def frequency(textWords):
    a=FreqDist(textWords)
    nbMots = 0
    for word in a :
        nbMots = nbMots + a[word]
    for i in a.keys():
        a[i]=a[i]/float(nbMots)
    return a

def frequencyWithTreshold(textWords, treshold):
    a=FreqDist(textWords)
    nbMots = 0
    wordsToRemove = []
    for word in a :
        if a[word] <= treshold :
            wordsToRemove.append(word)
        else :
            nbMots = nbMots + a[word]
    for word in wordsToRemove :
        del a[word]
    for i in a.keys():
        a[i]=a[i]/float(nbMots)
    return a

    
def textToDictionnary(text, blackList):
    return lemmatization(deleteStopWords(modifyText(getTextWords(delPunctuation(text)),blackList)))





t = """2.1. The many shades of quantumness of correlations
The simplest testbed for the study of correlations is that of a composite quantum system made
of two subsystems A and B, each associated with a (finite dimensional) Hilbert space HA and
HB, respectively. If the system is prepared in a pure quantum state |ψiAB ∈ HAB, where the
Hilbert space of the composite system is defined as the tensor product HAB = HA ⊗ HB of
the marginal Hilbert spaces, then essentially two possibilities can occur. The first is that the
two subsystems are completely independent, in which case the state takes the form of a tensor
product state |ψiAB = |αiA ⊗ |βiB
, with |αiA ∈ HA and |βiB ∈ HB. In this case there are
no correlations of any form (classical or quantum) between the two parts of the composite
system. The second possibility is that, instead, there exists no local state for A and B such that
the global state can be written in tensor product form,
|ψiAB , |αiA ⊗ |βiB
. (1)
In this case, |ψiAB describes an entangled state of the two subsystems A and B. Entanglement
encompasses any possible form of correlations in pure bipartite states, and can manifest in
different yet equivalent ways. For instance, every pure entangled state is nonlocal, meaning
that it can violate a Bell inequality [15]. Similarly, every pure entangled state is necessarily
disturbed by the action of any possible local measurement [6, 7]. Therefore, entanglement,
nonlocality, and QCs are generally synonymous for pure bipartite states.
As illustrated in Fig. 1, the situation is subtler and richer in case A and B are globally
prepared in a mixed state, described by a density matrix ρAB ∈ DAB, where DAB denotes the
Measures and applications of quantum correlations 7
convex set of all density operators acting on HAB. The state ρAB is separable, or unentangled,
if it can be prepared by means of local operations and classical communication (LOCC), i.e.,
if it takes the form
ρAB =
X
i
piς
(i)
A
⊗ τ
(i)
B
, (2)
with {pi} a probability distribution, and quantum states {ς
(i)
A
} of A and {τ
(i)
B
} of B. The set
SAB ⊂ DAB of separable states is constituted therefore by all states ρAB of the form given by
Eq. (2),
SAB =
n
ρAB | ρAB =
X
i
piς
(i)
A
⊗ τ
(i)
B
o
. (3)
Any other state ρAB < SAB is entangled. Mixed entangled states are hence defined as those
which cannot be decomposed as a convex mixture of product states. Notice that, unlike the
special case of pure states, the set of separable states is in general strictly larger than the set
of product states, SAB ⊃ PAB, where
PAB =
n
ρAB | ρAB = ρA ⊗ ρB
o
. (4)
Entanglement, one of the most fundamental resources of quantum information theory,
can be then recognised as a direct consequence of two key ingredients of quantum mechanics:
the superposition principle and the tensorial structure of the Hilbert space. We defer the reader
to [3] for a comprehensive review on entanglement, and to [16] for a compendium of the most
widely adopted entanglement measures. Within the set of entangled states, one can further
distinguish some layers of more stringent forms of non-classicality. In particular, some but
not all entangled states are steerable, and some but not all steerable states are nonlocal.
Steering, i.e. the possibility of manipulating the state of one subsystem by making
measurements on the other, captures the original essence of inseparability adversed by
Einstein, Podolsky and Rosen (EPR) [17] and appreciated by Schrodinger [18], and has been ¨
recently formalised in the modern language of quantum information theory [19]. It is an
asymmetric form of correlations, which means that some states can be steered from A to B but
not the other way around. The reader may refer to [4] for a recent review on EPR steering.
On the other hand, nonlocality, intended as a violation of EPR local realism [17],
represents the most radical departure from a classical description of the world, and has
received considerable attention in the last half century since Bell’s 1964 theorem [20].
Recently, a triplet of experiments demonstrating Bell nonlocality free of traditional loopholes
have been accomplished [21, 22, 23], confirming the predictions of quantum theory.
Nonlocality, like entanglement, is a symmetric type of correlations, invariant under the swap
of parties A and B. The reader is referred to [5] for a review on nonlocality and its applications.
As remarked, here we are mainly interested in signatures of quantumness beyond
entanglement. Therefore, an important question we should consider is: Are the correlations
in separable states completely classical? In the following we argue that, in general, this is not
the case. The only states which may be regarded as classically correlated form a negligible
corner of the subset of separable states, and will be formally defined in the next subsection.
2.2. Classically correlated states
Consider a composite system consisting of a classical bit and a quantum bit (qubit). For
convenience, we shall adopt the same formalism for both. The classical bit can either be in
the state |0i or in the state |1i, representing e.g. “off” or “on” in modern binary electronics and
communications. If the classical bit is in |0i, one can write the composite state as |0i h0|A ⊗ρB,
Measures and applications of quantum correlations 8
where we have identified the classical bit as subsystem A and the qubit as subsystem B, with
ρB a quantum state. However, if the state of the classical bit is unknown, then the composite
state ρAB is a statistical mixture, i.e.
ρAB = p0 |0i h0|A ⊗ ρ
(0)
B
+ p1 |1i h1|A ⊗ ρ
(1)
B
, (5)
where p0 and p1 are probabilities adding up to one, while ρ
(0)
B
and ρ
(1)
B
denote the state of the
quantum bit B when the classical bit A is in |0i and |1i, respectively. This is an example of
what we call a classical-quantum state, or classical on A, since subsystem A can be thought
of as classical. Equivalently, we can say that ρAB is classically correlated with respect to
subsystem A, the motivation for this terminology becoming clear soon.
Going beyond just bits, one can think about any classical system as consisting of a
collection of distinct states, which can be represented using an orthonormal basis {|ii}. Any
classical-quantum state can then be written as a statistical mixture in the following way [24]"""

w= textToDictionnary(t, [])
d = frequency(w)
e = frequencyWithTreshold(w, 2)


for word in d :
    if word in e :
        print(word)