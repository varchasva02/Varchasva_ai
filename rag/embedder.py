from functools import lru_cache

from sentence_transformers import SentenceTransformer

from .chunker import create_semantic_chunks


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_embedding_model():
    """Load the embedding model once and reuse it."""
    return SentenceTransformer(MODEL_NAME)


@lru_cache(maxsize=1)
def create_embeddings():
    """Create embeddings once and reuse them."""

    chunks = create_semantic_chunks()

    model = get_embedding_model()

    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    return chunks, embeddings


if __name__ == "__main__":

    chunks, embeddings = create_embeddings()

    print("\nEmbedding generation complete.")
    print("Number of chunks:", len(chunks))
    print("Embedding shape:", embeddings.shape)
    print("Embedding dtype:", embeddings.dtype)

    print("\nFirst embedding:")
    print(embeddings[0])