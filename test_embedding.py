from src.embedding import generate_embeddings


sample_chunks = [
    "Artificial Intelligence is transforming the world.",
    "Machine Learning helps computers learn from data.",
    "Python is a popular programming language."
]


embeddings = generate_embeddings(sample_chunks)


print("\n===== EMBEDDING RESULTS =====")

print("Number of chunks:", len(sample_chunks))

print("Embedding shape:", embeddings.shape)

print("\nFirst embedding (first 10 values):")
print(embeddings[0][:10])

print("\n===== TEST SUCCESSFUL =====")