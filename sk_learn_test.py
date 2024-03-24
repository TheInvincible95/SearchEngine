from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Example documents
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
# Initialize TF-IDF vectorizer
vectorizer = TfidfVectorizer()

# Fit-transform the documents to obtain TF-IDF vectors
tfidf_matrix = vectorizer.fit_transform(documents.values())

query = "artificial intelligence"
query_tfidf_matrix = vectorizer.transform([query])
# Compute cosine similarity between documents
cosine_similarities = cosine_similarity(tfidf_matrix, query_tfidf_matrix)
# Print cosine similarity matrix
print("Cosine Similarity Matrix:")
print(cosine_similarities)

# sorted_documents = sorted(documents.items(), key=lambda x: rating[x[0]], reverse=True)
# print(f"Query:{query}")
# for name, doc in sorted_documents:
#     print(f'Rating:{rating[name] : 4f}\nDocument:"{doc}"')