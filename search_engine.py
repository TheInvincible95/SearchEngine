# from nltk import download
# download('punkt')
from collections import defaultdict
from math import log
import json # For dump
from nltk.tokenize import word_tokenize
documents = {
    "0": "Artificial intelligence has revolutionized various industries.",
    "1": "The future of technology is driven by artificial intelligence.",
    "2": "Machine learning and AI are transforming businesses worldwide.",
    "3": "Advancements in robotics have paved the way for automation.",
    "4": "The role of data analytics in shaping the future of technology.",
    "5": "Healthy eating habits are essential for a balanced lifestyle.",
    "6": "Nutritious foods contribute to overall well-being and longevity.",
    "7": "The importance of incorporating fruits and vegetables into your diet.",
    "8": "Exploring different cuisines can be a delightful culinary experience.",
    "9": "Cooking techniques and recipes for preparing delicious meals at home.",
    "10": "Space exploration continues to unravel the mysteries of the universe.",
    "11": "The race to Mars: Challenges and opportunities for human colonization.",
    "12": "The wonders of astronomy: Discovering new celestial phenomena.",
    "13": "Exploring the vastness of the cosmos through powerful telescopes.",
    "14": "The impact of social media on modern communication and relationships.",
    "15": "Navigating the complexities of social media etiquette in the digital age.",
    "16": "The rise of influencer culture: Examining its implications on society.",
    "17": "Effective strategies for managing stress and promoting mental well-being.",
    "18": "Mindfulness and meditation practices for achieving inner peace and clarity.",
    "19": "The importance of self-care in maintaining physical and emotional health.",
}


def preprocess(string):
    return word_tokenize(string)


totalDocuments = len(documents)
documentFreq = defaultdict(
    int
)  # This will store (word -> count) where count no of documents word occurs in
allTermFreqs = (
    {}
)  # This will store (docName -> dict of term frequencies in that document)

for name, doc in documents.items():
    termFreq = defaultdict(
        int
    )  # This will store (word -> count) where count is for current document
    tokens = preprocess(doc)
    for tok in tokens:
        if tok not in termFreq:
            documentFreq[tok] += 1
        termFreq[tok] += 1
    allTermFreqs[name] = termFreq




with open("test.json", "w+") as fileDump:
    json.dump(allTermFreqs, fileDump)
with open("test2.json", "w+") as fileDump:
    json.dump(documentFreq, fileDump)


# Fotmulas from here: https://en.wikipedia.org/wiki/Tf%E2%80%93idf
# Can use a different one too
def TF(t, d):
    # TODO: Try different formulas from Wikipedia
    terms = allTermFreqs[d]
    f = terms.get(t) or 0  # Trying to access the element with [] will add it
    # TODO: Store the sum along with the document
    summation = 0
    for _, fi in terms.items():
        summation += fi
    return f / summation


def IDF(t):
    # TODO: Try different formulas from Wikipedia
    d = documentFreq.get(t) or 0
    return log(totalDocuments / (1 + d))

query = "artificial intelligence"
tokens = word_tokenize(query)
rating = {}
for name in documents:
    TF_IDF = 0
    for tok in tokens:
        # TODO Currently using addition to aggregate the scores, could use a different strategy
        TF_IDF += TF(tok, name) * IDF(tok) 
    rating[name] = TF_IDF

sorted_documents = sorted(documents.items(), key=lambda x: rating[x[0]], reverse=True)
print(f"Query:{query}")
for name, doc in sorted_documents:
    print(f"Rating:{rating[name]}\nDocument:\"{doc}\"")
