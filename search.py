from collections import defaultdict
from math import log
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


# TODO: Currently all vectors are stored as (string , number) pairs. We could replace this if we use a consitent word->number function
class Document:
    def __init__(self, text):
        self.text = text  # We don't really need to store this
        self.term_freq = self.preprocess(text)

    def preprocess(self, string):
        tokens = word_tokenize(string)
        tokens = [token.lower() for token in tokens]

        # Remove stop words
        stop_words = set(stopwords.words("english"))
        tokens = [token for token in tokens if token not in stop_words]
        term_freq = defaultdict(int)
        for token in tokens:
            term_freq[token] += 1
        return term_freq


class Searcher:
    def __init__(self):
        self.documents = []
        self.total_documents = 0
        self.document_freq = defaultdict(int)

    def add_document(self, text):
        doc = Document(text)
        self.documents.append(doc)
        self.total_documents += 1

        for term in doc.term_freq:
            self.document_freq[term] += 1
        return self.total_documents - 1

    def tf(self, term, doc):
        return doc.term_freq.get(term, 0) / float(sum(doc.term_freq.values()))

    def idf(self, term):
        return log(self.total_documents / float((1 + self.document_freq.get(term, 0))))

    def tf_idf(self, term, doc):
        return self.tf(term, doc) * self.idf(term)

    def _tf_idf_vector(self, document):
        tf_idf_vector = {}
        for term in document.term_freq:
            tf_idf_vector[term] = self.tf_idf(term, document)
        return tf_idf_vector

    def get_tf_idf_vector(self, doc_id):
        if doc_id < 0 or doc_id >= len(self.documents):
            raise ValueError("Invalid document ID")
        doc = self.documents[doc_id]
        return self._tf_idf_vector(doc)

    def _cosine_similarity_internal(self, doc1_tf_idf, doc2_tf_idf):
        dot_product = sum(
            doc1_tf_idf.get(term, 0) * doc2_tf_idf.get(term, 0) for term in doc1_tf_idf
        )
        mag1 = sum(val**2 for val in doc1_tf_idf.values()) ** 0.5
        mag2 = sum(val**2 for val in doc2_tf_idf.values()) ** 0.5
        if mag1 == 0 or mag2 == 0:
            return 0
        return dot_product / float(mag1 * mag2)

    def cosine_similarity(self, doc_id1, doc_id2):
        doc1_tf_idf = self.get_tf_idf_vector(doc_id1)
        doc2_tf_idf = self.get_tf_idf_vector(doc_id2)
        return self._cosine_similarity_internal(doc1_tf_idf, doc2_tf_idf)

    def search(self, query):
        query_doc = Document(query)
        query_tf_idf = self._tf_idf_vector(query_doc)
        rankings = []
        for i, doc in enumerate(self.documents):
            doc_tf_idf = self.get_tf_idf_vector(i)
            similarity = self._cosine_similarity_internal(query_tf_idf, doc_tf_idf)
            rankings.append((i, similarity))

        rankings.sort(key=lambda x: x[1], reverse=True)
        return rankings


if __name__ == "__main__":
    # Create a Searcher instance
    search_engine = Searcher()
    # Add some example documents
    docs = [
        "Artificial intelligence has revolutionized various industries.",
        "The future of technology is driven by artificial intelligence.",
        "Machine learning and AI are transforming businesses worldwide.",
        "Advancements in robotics have paved the way for automation.",
        "The role of data analytics in shaping the future of technology.",
        "Healthy eating habits are essential for a balanced lifestyle.",
        "Nutritious foods contribute to overall well-being and longevity.",
        "The importance of incorporating fruits and vegetables into your diet.",
        "Exploring different cuisines can be a delightful culinary experience.",
        "Cooking techniques and recipes for preparing delicious meals at home.",
        "Space exploration continues to unravel the mysteries of the universe.",
        "The race to Mars: Challenges and opportunities for human colonization.",
        "The wonders of astronomy: Discovering new celestial phenomena.",
        "Exploring the vastness of the cosmos through powerful telescopes.",
        "The impact of social media on modern communication and relationships.",
        "Navigating the complexities of social media etiquette in the digital age.",
        "The rise of influencer culture: Examining its implications on society.",
        "Effective strategies for managing stress and promoting mental well-being.",
        "Mindfulness and meditation practices for achieving inner peace and clarity.",
        "The importance of self-care in maintaining physical and emotional health.",
    ]
    for d in docs:
        search_engine.add_document(d)

    # Test a query
    query = "artificial intelligence and machine learning"
    results = search_engine.search(query)
    print("Query:", query)
    print("Results:", results)
