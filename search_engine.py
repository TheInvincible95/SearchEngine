# from nltk import download
# download('stopwords')
# download('punkt')

from collections import defaultdict
from math import log
import json  # For dump
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# from transformers import BertTokenizer # Not used
import sys

import corpusToDict as ctd
import search as sch

# to store the state of the searcher class, so as to not recompute it everytime the code runs
import pickle
import os

# ============================================================== Run this when file is imported, as initialisation ==================================================================

# this part takes ~48ms, so dont store it, and compute it each time the code is run
# ---------------------------------------------------------------------------------
# getting the corpus here:
filePath = "./Corpus.csv"

corpus = ctd.getCorpus(filePath)

documents = {}

for i in range(1, len(corpus)):

    text = corpus[i][0]
    documents[i - 1] = text

# ---------------------------------------------------------------------------------


# This part takes about 6s
# if there is no pickle of a previously computed searcher class, compute it and store it in a pickle
# reduces the runtime of this part of code from ~6s to ~1s
def raveQuery(category, query):
    if not os.path.exists("./searcherPickle.pkl"):

        # Create a Searcher instance
        search_engine = sch.Searcher()

        for name, doc in documents.items():
            cat = corpus[name + 1][1]
            search_engine.add_document(doc, name, cat)
        search_engine.avgdlcalc(cat)

        # create the pickle file
        with open("searcherPickle.pkl", "wb") as file:
            pickle.dump(search_engine, file)

    # if the searcher class already computed stuff, and stored it in a pickle, directly read the searcher class from the pickle:
    else:
        with open("searcherPickle.pkl", "rb") as file:
            search_engine = pickle.load(file)

    # ===================================================================================================================================================================================

    # return the results of a query
    return search_engine.search(category, query)
