import faiss
import numpy as np
from functools import lru_cache

from .embedder import create_embeddings


@lru_cache(maxsize=1)
def build_vector_store():
    """Build the FAISS vector store once and reuse it."""

    chunks, embeddings = create_embeddings()

    # Convert embeddings to float32 for FAISS
    embeddings = np.asarray(embeddings, dtype="float32")

    # Number of dimensions in each embedding
    dimension = embeddings.shape[1]

    # Inner Product works as cosine similarity
    # because our embeddings are normalized.
    index = faiss.IndexFlatIP(dimension)

    # Add all embeddings to FAISS
    index.add(embeddings)

    return index, chunks


if __name__ == "__main__":

    index, chunks = build_vector_store()

    print("\nFAISS index created successfully.")
    print("Number of vectors:", index.ntotal)
    print("Vector dimension:", index.d)