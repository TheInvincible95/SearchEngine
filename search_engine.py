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

# documents = {
#     "0": "Artificial intelligence has revolutionized various industries.",
#     "1": "The future of technology is driven by artificial intelligence.",
#     "2": "Machine learning and AI are transforming businesses worldwide.",
#     "3": "Advancements in robotics have paved the way for automation.",
#     "4": "The role of data analytics in shaping the future of technology.",
#     "5": "Healthy eating habits are essential for a balanced lifestyle.",
#     "6": "Nutritious foods contribute to overall well-being and longevity.",
#     "7": "The importance of incorporating fruits and vegetables into your diet.",
#     "8": "Exploring different cuisines can be a delightful culinary experience.",
#     "9": "Cooking techniques and recipes for preparing delicious meals at home.",
#     "10": "Space exploration continues to unravel the mysteries of the universe.",
#     "11": "The race to Mars: Challenges and opportunities for human colonization.",
#     "12": "The wonders of astronomy: Discovering new celestial phenomena.",
#     "13": "Exploring the vastness of the cosmos through powerful telescopes.",
#     "14": "The impact of social media on modern communication and relationships.",
#     "15": "Navigating the complexities of social media etiquette in the digital age.",
#     "16": "The rise of influencer culture: Examining its implications on society.",
#     "17": "Effective strategies for managing stress and promoting mental well-being.",
#     "18": "Mindfulness and meditation practices for achieving inner peace and clarity.",
#     "19": "The importance of self-care in maintaining physical and emotional health.",
# }

# getting the corpus here:
filePath = "./Corpus.csv"

corpus = ctd.getCorpus(filePath)

documents = {}

for i in range(1, len(corpus)):

    text = corpus[i][0]
    documents[i - 1] = text

# Create a Searcher instance
search_engine = sch.Searcher()

for name, doc in documents.items():
    search_engine.add_document(doc)
search_engine.avgdlcalc()

# return the results of a query


def raveQuery(query):
    return search_engine.search(query)
