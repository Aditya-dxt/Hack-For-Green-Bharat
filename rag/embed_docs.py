from sentence_transformers import SentenceTransformer
from chunk_docs import load_and_chunk_documents

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_documents():
    chunks = load_and_chunk_documents()

    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts)

    embedded_chunks = []
    for i, chunk in enumerate(chunks):
        embedded_chunks.append({
            "text": chunk["text"],
            "source": chunk["source"],
            "embedding": embeddings[i]
        })

    return embedded_chunks


if __name__ == "__main__":
    embedded_chunks = embed_documents()
    print("TOTAL EMBEDDINGS:", len(embedded_chunks))
    print("Example embedding length:", len(embedded_chunks[0]["embedding"]))

