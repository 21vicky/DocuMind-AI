from src.text_chunker import split_text_into_chunks

sample_text = """
Artificial Intelligence is transforming the world.
Machine Learning is a subset of Artificial Intelligence.
Deep Learning uses neural networks to learn complex patterns.
Natural Language Processing helps computers understand human language.
"""

chunks = split_text_into_chunks(
    sample_text,
    chunk_size=100,
    overlap=20
)

print("\n===== TEXT CHUNKS =====")

for index, chunk in enumerate(chunks, start=1):
    print(f"\nChunk {index}:")
    print(chunk)

print("\n===== TOTAL CHUNKS =====")
print(len(chunks))