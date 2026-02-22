from sentence_transformers import SentenceTransformer
from chunk_docs import load_and_chunk_documents
from embed_docs import embed_documents
import numpy as np

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def search(query, top_k=3):
    # Embed query
    query_embedding = model.encode(query)

    # Load document embeddings
    embedded_chunks = embed_documents()

    # Compute similarity
    scores = []
    for chunk in embedded_chunks:
        score = cosine_similarity(query_embedding, chunk["embedding"])
        scores.append((score, chunk["text"], chunk["source"]))

    # Sort by similarity (highest first)
    scores.sort(reverse=True, key=lambda x: x[0])

    return scores[:top_k]


if __name__ == "__main__":
    question = "Is AQI 320 dangerous for children?"

    results = search(question)

    print("QUESTION:", question)
    print("-" * 50)

    for score, text, source in results:
        print(f"Score: {score:.3f}")
        print(f"Text: {text}")
        print(f"Source: {source}")
        print("-" * 50)

