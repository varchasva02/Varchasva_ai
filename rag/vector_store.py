import json
from pathlib import Path
from functools import lru_cache
import faiss
import numpy as np

# File paths for persisting precomputed artifacts
CURRENT_DIR = Path(__file__).parent
INDEX_PATH = CURRENT_DIR / "faiss_index.bin"
CHUNKS_PATH = CURRENT_DIR / "chunks.json"


def save_vector_store(index, chunks, index_path=INDEX_PATH, chunks_path=CHUNKS_PATH):
    """Persist FAISS index and chunks to disk."""
    faiss.write_index(index, str(index_path))
    with open(chunks_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)


def generate_and_save_vector_store(index_path=INDEX_PATH, chunks_path=CHUNKS_PATH):
    """Generate embeddings for all documents, build FAISS index, and persist to disk."""
    try:
        from .embedder import create_embeddings
    except ImportError:
        from rag.embedder import create_embeddings

    print("Generating document embeddings and building FAISS index...")
    chunks, embeddings = create_embeddings()

    # Convert embeddings to float32 for FAISS
    embeddings = np.asarray(embeddings, dtype="float32")
    dimension = embeddings.shape[1]

    # Inner Product works as cosine similarity because embeddings are normalized
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    save_vector_store(index, chunks, index_path, chunks_path)
    print(f"Persisted FAISS index ({index.ntotal} vectors) -> {index_path}")
    print(f"Persisted chunks ({len(chunks)} chunks) -> {chunks_path}")
    return index, chunks


def load_vector_store(index_path=INDEX_PATH, chunks_path=CHUNKS_PATH):
    """Load persisted FAISS index and chunks from disk without generating embeddings."""
    if not index_path.exists():
        raise FileNotFoundError(
            f"FAISS index file not found at '{index_path}'. "
            "Run 'python -m rag.vector_store' locally to generate and persist the vector store."
        )

    if not chunks_path.exists():
        raise FileNotFoundError(
            f"Chunks file not found at '{chunks_path}'. "
            "Run 'python -m rag.vector_store' locally to generate and persist the chunks."
        )

    index = faiss.read_index(str(index_path))
    with open(chunks_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    return index, chunks


@lru_cache(maxsize=1)
def build_vector_store():
    """Load the precomputed vector store and chunks once and reuse them in memory."""
    return load_vector_store()


if __name__ == "__main__":
    index, chunks = generate_and_save_vector_store()
    print("\nVerification:")
    print("Number of vectors in FAISS index:", index.ntotal)
    print("Vector dimension:", index.d)
    print("Number of chunks:", len(chunks))