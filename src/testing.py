# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 17:58:34 2016

@author: loic
"""

import os
import categoryVisualization
import retrieveCategories

random = """How random is a real? Given two reals, which is more random? How should
we even try to quantify these questions, and how do various choices of
measurement relate? Once we have reasonable measuring devices, and, using
these devices, we divide the reals into equivalence classes of the same
“degree of randomness” what do the resulting structures look like? Once
we measure the level of randomness how does the level of randomness relate
to classical measures of complexity Turing degrees of unsolvability?
Should it be the case that high levels of randomness mean high levels of
complexity in terms of computational power, or low levels of complexity?
Conversely should the structures of computability such as the degrees and
the computably enumerable sets have anything to say about randomness
for reals?
These were the kinds of questions motivating the research which is represented
in this book. While some fundamental questions remain open,
nevertheless we now have a reasonable insight into many of these questions,
and the resulting body of work is both beautiful and has a number
of rather deep theorems.
We all see a sequence like 11111111111 . . . and another like
101101011101010111100001010100010111 . . . and feel that the second (obtained
by the first author by a coin toss) is more random than the first.
However, in terms of measure theory, each is equally likely. It is a deep and
fundamental question to try to understand why some sequence might be
“random” and another might be “lawful,” and, moreover, how to quantify
our intuition into a meaningful mathematical notion.
xvi 3. Introduction
The roots of the study of algorithmic randomness -questions like thesego
back to the work of von Mises at the dawn of the 20th century. In a
remarkable paper [317], von Mises argued that a a random real should be
what we would now call stochastic in the sense that it ought to obey all
“reasonable” statistical tests. For instance, the number of zeroes in the
sequence 6 n asymptotically be the same as the number of ones. Actually
he expressed his ideas about Kollektivs in terms of “acceptable selection
rules.” He observed that any countable collection could be beaten, but at
the time it was unclear what types of selection rules should be admissible.
There seemed to him no canonical choice.
Later, with the development of computability/recursive function theory,
it seemed that the notion of algorithmic randomness is intimately tied to
the notion of a computable function. This was argued by Church [52] and
others. Church made the connection with the theory of computability by
suggesting that one should take all computable stochastic properties. A blow
to this program was made by Ville [312], who pointed out that no matter
what admissible rules were chosen there would be reals which were random
relative to the chosen rules, yet had properties that would demonstrate that
the real was not random.
In a sweeping generalization, Martin-L¨of [198] noted that selection rules,
and similar stochastic approaches are special kinds of measure zero sets,
and the this approach culminated with Martin-L¨of’s definition of randomness
as reals that avoided certain effectively presented measure 0
sets.
Exactly which choice of “effectively presented measure 0 sets” are appropriate
now becomes the issue and manipulating the acceptable kinds of
measure 0 sets allows one to calibrate randomness in a natural way.
In this book we will consider a number of such variations, n-randomness,
arithmetical randomness, s-randomness (associated with Hausdorff dimension),
Schnorr randomness, Kurtz randomness and the like.
There are subtle and deep questions about the measure-theoretical approach
and its relationship with the original stochastic approach. We will
discuss these relationships later in the book.
The evolution and clarification of many these notions is carefully
discussed in the PhD Thesis of Michael van Lambalgen [314].
What we call the measure-theoretical approach is only one of the three
basic approaches to algorithmic randomness. They are in terms of unpredictability,
typicalness, and incompressibility. Strangely, the last was the
first to be adequately addressed. Kolmogorov [151], gave the first basic results
on what we now call Kolmogorov complexity, though these results
were foreshadowed by Ray Solomonoff [282]. Roughly, the idea is that a
string should be random only if it cannot be compressed by some program.
This leads to the now “standard” notion of Kolmogorov complexity of
a string, σ, namely the length of shortest program τ such that U(τ ) = σ.
Then a string is random iff its Kolmogorov complexity is the same size
3. Introduction xvii
as its length. Kolmogorov proved basic results such as this is well-defined
notion since, up to a constant, the choice of universal machine does not
matter."""

info = """This book is devoted to the theory of probabilistic information measures and
their application to coding theorems for information sources and noisy channels.
The eventual goal is a general development of Shannon’s mathematical theory
of communication, but much of the space is devoted to the tools and methods
required to prove the Shannon coding theorems. These tools form an area common
to ergodic theory and information theory and comprise several quantitative
notions of the information in random variables, random processes, and dynamical
systems. Examples are entropy, mutual information, conditional entropy,
conditional information, and relative entropy (discrimination, Kullback-Leibler
information), along with the limiting normalized versions of these quantities
such as entropy rate and information rate. When considering multiple random
objects, in addition to information we will be concerned with the distance or
distortion between the random objects, that is, the accuracy of the representation
of one random object by another. Much of the book is concerned with the
properties of these quantities, especially the long term asymptotic behavior of
average information and distortion, where both sample averages and probabilistic
averages are of interest.
The book has been strongly influenced by M. S. Pinsker’s classic Information
and Information Stability of Random Variables and Processes and by the seminal
work of A. N. Kolmogorov, I. M. Gelfand, A. M. Yaglom, and R. L. Dobrushin on
information measures for abstract alphabets and their convergence properties.
Many of the results herein are extensions of their generalizations of Shannon’s
original results. The mathematical models of this treatment are more general
than traditional treatments in that nonstationary and nonergodic information
processes are treated. The models are somewhat less general than those of the
Soviet school of information theory in the sense that standard alphabets rather
than completely abstract alphabets are considered. This restriction, however,
permits many stronger results as well as the extension to nonergodic processes.
In addition, the assumption of standard spaces simplifies many proofs and such
spaces include as examples virtually all examples of engineering interest.
The information convergence results are combined with ergodic theorems
to prove general Shannon coding theorems for sources and channels. The results
are not the most general known and the converses are not the strongest
available, but they are sufficently general to cover most systems encountered
in applications and they provide an introduction to recent extensions requiring
ix
x PROLOGUE
significant additional mathematical machinery. Several of the generalizations
have not previously been treated in book form. Examples of novel topics for an
information theory text include asymptotic mean stationary sources, one-sided
sources as well as two-sided sources, nonergodic sources, ¯d-continuous channels,
and sliding block or stationary codes . Another novel aspect is the use of recent
proofs of general Shannon-McMillan-Breiman theorems which do not use martingale
theory — a coding proof of Ornstein and Weiss [118] is used to prove
the almost everywhere convergence of sample entropy for discrete alphabet processes
and a variation on the sandwich approach of Algoet and Cover [7] is used
to prove the convergence of relative entropy densities for general standard alphabet
processes. Both results are proved for asymptotically mean stationary
processes which need not be ergodic.
This material can be considered as a sequel to my book Probability, Random
Processes, and Ergodic Properties [51] wherein the prerequisite results on probability,
standard spaces, and ordinary ergodic properties may be found. This
book is self contained with the exception of common (and a few less common)
results which may be found in the first book.
It is my hope that the book will interest engineers in some of the mathematical
aspects and general models of the theory and mathematicians in some of
the important engineering applications of performance bounds and code design
for communication systems.
Information theory, the mathematical theory of communication, has two
primary goals: The first is the development of the fundamental theoretical limits
on the achievable performance when communicating a given information
source over a given communications channel using coding schemes from within
a prescribed class. The second goal is the development of coding schemes that
provide performance that is reasonably good in comparison with the optimal
performance given by the theory. Information theory was born in a surprisingly
rich state in the classic papers of Claude E. Shannon [131] [132] which
contained the basic results for simple memoryless sources and channels and introduced
more general communication systems models, including finite state
sources and channels. The key tools used to prove the original results and many
of those that followed were special cases of the ergodic theorem and a new variation
of the ergodic theorem which considered sample averages of a measure of
the entropy or self information in a process.
Information theory can be viewed as simply a branch of applied probability
theory. Because of its dependence on ergodic theorems, however, it can also be
viewed as a branch of ergodic theory, the theory of invariant transformations
and transformations related to invariant transformations. In order to develop
the ergodic theory example of principal interest to information theory, suppose
that one has a random process, which for the moment we consider as a sample
space or ensemble of possible output sequences together with a probability
measure on events composed of collections of such sequences. The shift is the
transformation on this space of sequences that takes a sequence and produces a
new sequence by shifting the first sequence a single time unit to the left. In other
PROLOGUE xi
words, the shift transformation is a mathematical model for the effect of time
on a data sequence. If the probability of any sequence event is unchanged by
shifting the event, that is, by shifting all of the sequences in the event, then the
shift transformation is said to be invariant and the random process is said to be
stationary. Thus the theory of stationary random processes can be considered as
a subset of ergodic theory. Transformations that are not actually invariant (random
processes which are not actually stationary) can be considered using similar
techniques by studying transformations which are almost invariant, which are
invariant in an asymptotic sense, or which are dominated or asymptotically
dominated in some sense by an invariant transformation. This generality can
be important as many real processes are not well modeled as being stationary.
Examples are processes with transients, processes that have been parsed into
blocks and coded, processes that have been encoded using variable-length codes"""


textList = [random, info]

uris1 = retrieveCategories.getURIs(random)
categories1 = retrieveCategories.getCategories(uris1[0], uris1[1])

uris2 = retrieveCategories.getURIs(info)
categories2 = retrieveCategories.getCategories(uris2[0], uris2[1])

categories = []
for category in categories1[0]:
    if category in categories2[0]:
        categories.append(category)

l = categoryVisualization.getLinkedWord("Randomness", textList)
p=categoryVisualization.getTextWithMostOccurenceOf("randomness", "Randomness", textList )