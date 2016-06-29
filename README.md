# aps
Analysis of scientific papers and results visualization

# Plugins:

* nltk

* latexcodec

* Flask

* pdfMiner

* bibtexparser

* rdflib

* pyspotlight

* datetime

→ ```sudo pip install nltk latexcodec Flask pdfMiner bibtexparser rdflib pyspotlight dateutil```



# How to view the wordcloud:

1) You will need a command line inside the source folder. You can execute ```cd aps/``` after cloning our repository.

2) Launch ```python src/server.py``` to launch the Flask server.

3) Go to [http://localhost:5000/](http://localhost:5000/), this is the index page

4) Launch the computation by going to [http://localhost:5000/init_wordcloud](http://localhost:5000/init_wordcloud). You can follow the computations in the console.

5) When the page is done loading, it will print something like ```Word Cloud for biblio.bib done```. you can check the word cloud on the index page.

6) Enjoy!

# How to view the coauthoring graph:

1) Make sure you have **telecom.bib** in your **aps/data** folder.
(If you don't, you can put another **.bib** file and rename it)

2) You will need a command line inside the source folder. You can execute ```cd aps/``` after cloning our repository.

3) Launch ```python src/main_graph.py``` to launch the computations.

4) Launch ```python src/server.py``` to start the server if the server isn't already on. If it's already on, there's no point restarting it as it refreshes.

5) Go to [http://localhost:5000/](http://localhost:5000/), this is the index page

6) Enjoy!
# Contributors:

Loïc Herbelot

Antoine Sueur

Romeo Brofiga

Adrien Lagasse


