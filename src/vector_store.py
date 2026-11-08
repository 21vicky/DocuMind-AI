import faiss
import numpy as np

from src.embedding import generate_embeddings


# ============================================================
# BUILD FAISS VECTOR DATABASE
# ============================================================

def build_vector_store(chunks, embeddings):

    if not chunks or len(chunks) != len(embeddings):
        raise ValueError(
            "Chunks and embeddings must have matching lengths."
        )

    # Convert embeddings into float32
    embeddings = np.asarray(
        embeddings,
        dtype=np.float32
    ).copy()

    # Normalize vectors for cosine similarity
    faiss.normalize_L2(embeddings)

    # Get embedding dimension
    dimension = embeddings.shape[1]

    # Create FAISS index
    index = faiss.IndexFlatIP(dimension)

    # Store embeddings
    index.add(embeddings)

    return index


# ============================================================
# SEARCH SIMILAR DOCUMENT CHUNKS
# ============================================================

def search_similar_chunks(
    query,
    index,
    chunks,
    top_k=3
):

    if not query.strip():
        raise ValueError(
            "Search query cannot be empty."
        )

    if index.ntotal == 0:
        return []

    # Generate query embedding
    query_embedding = generate_embeddings([query])

    query_embedding = np.asarray(
        query_embedding,
        dtype=np.float32
    ).copy()

    # Normalize query vector
    faiss.normalize_L2(query_embedding)

    # Search FAISS
    top_k = min(top_k, index.ntotal)

    scores, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    # Collect search results
    for score, idx in zip(scores[0], indices[0]):

        if idx == -1:
            continue

        results.append({
            "text": chunks[int(idx)],
            "score": float(score),
            "chunk_index": int(idx)
        })

    return results