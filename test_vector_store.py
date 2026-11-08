from src.embedding import generate_embeddings

from src.vector_store import (
    build_vector_store,
    search_similar_chunks
)


# Sample document chunks
chunks = [
    "Artificial Intelligence enables machines to perform tasks that normally require human intelligence.",
    "Machine Learning is a branch of AI that allows computers to learn from data.",
    "Deep Learning uses neural networks with multiple layers.",
    "Python is a popular programming language used in AI and data science.",
    "Natural Language Processing helps computers understand human language."
]


# Generate embeddings
embeddings = generate_embeddings(chunks)


# Build FAISS database
index = build_vector_store(chunks, embeddings)


print("\n===== FAISS DATABASE =====")
print("Total vectors stored:", index.ntotal)


# Ask a question
query = "How do computers learn from data?"


print("\n===== SEARCH RESULTS =====")
print("Question:", query)


results = search_similar_chunks(
    query,
    index,
    chunks,
    top_k=3
)


for i, result in enumerate(results, start=1):

    print(f"\nResult {i}")
    print("Similarity Score:", round(result["score"], 4))
    print("Text:", result["text"])


print("\n===== TEST SUCCESSFUL =====")