"""
SMART PADDY PROJECT
RAG Embeddings

Purpose:
    Convert RAG text chunks into numerical vectors
    using Sentence Transformers.

Model:
    sentence-transformers/all-MiniLM-L6-v2
"""

from typing import List, Dict

import numpy as np
from sentence_transformers import SentenceTransformer

from rag.config import EMBEDDING_MODEL_NAME
from rag.chunking import chunk_all_documents


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

def load_embedding_model() -> SentenceTransformer:
    """
    Load the Sentence Transformer embedding model.
    """

    print()
    print("Loading embedding model...")
    print(f"Model: {EMBEDDING_MODEL_NAME}")

    model = SentenceTransformer(
        EMBEDDING_MODEL_NAME
    )

    print("Embedding model loaded successfully.")

    return model


# ============================================================
# EXTRACT TEXT FROM CHUNKS
# ============================================================

def get_chunk_texts(
    chunks: List[Dict],
) -> List[str]:
    """
    Extract text from chunk records.
    """

    return [
        chunk["text"]
        for chunk in chunks
    ]


# ============================================================
# CREATE EMBEDDINGS
# ============================================================

def create_embeddings(
    chunks: List[Dict],
    model: SentenceTransformer,
) -> np.ndarray:
    """
    Convert all chunk texts into embedding vectors.
    """

    if not chunks:
        raise ValueError(
            "No chunks available for embedding."
        )

    texts = get_chunk_texts(chunks)

    print()
    print(
        f"Creating embeddings for "
        f"{len(texts)} chunks..."
    )

    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    embeddings = np.asarray(
        embeddings,
        dtype="float32",
    )

    print()
    print("Embeddings created successfully.")

    print(
        f"Number of vectors : {embeddings.shape[0]}"
    )

    print(
        f"Vector dimension  : {embeddings.shape[1]}"
    )

    return embeddings


# ============================================================
# VALIDATE EMBEDDINGS
# ============================================================

def validate_embeddings(
    embeddings: np.ndarray,
    chunks: List[Dict],
) -> bool:
    """
    Validate embedding matrix.
    """

    if embeddings is None:

        print("ERROR: Embeddings are None.")

        return False

    if not isinstance(
        embeddings,
        np.ndarray,
    ):

        print(
            "ERROR: Embeddings are not "
            "a NumPy array."
        )

        return False

    if embeddings.ndim != 2:

        print(
            "ERROR: Embeddings must be "
            "a 2-dimensional array."
        )

        return False

    if len(chunks) != embeddings.shape[0]:

        print(
            "ERROR: Number of chunks and "
            "number of embeddings do not match."
        )

        print(
            f"Chunks      : {len(chunks)}"
        )

        print(
            f"Embeddings  : {embeddings.shape[0]}"
        )

        return False

    if embeddings.shape[1] <= 0:

        print(
            "ERROR: Embedding dimension is invalid."
        )

        return False

    if not np.isfinite(embeddings).all():

        print(
            "ERROR: Embeddings contain "
            "NaN or infinite values."
        )

        return False

    return True


# ============================================================
# EMBEDDING SEARCH TEST
# ============================================================

def create_query_embedding(
    query: str,
    model: SentenceTransformer,
) -> np.ndarray:
    """
    Create an embedding for a user query.

    This will later be used by the RAG retriever.
    """

    if not query.strip():

        raise ValueError(
            "Query cannot be empty."
        )

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    query_embedding = np.asarray(
        query_embedding,
        dtype="float32",
    )

    return query_embedding


# ============================================================
# MAIN TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("SMART PADDY - RAG EMBEDDING TEST")
    print("=" * 70)

    try:

        # ----------------------------------------------------
        # Load chunks
        # ----------------------------------------------------

        print()
        print("Loading RAG chunks...")

        chunks = chunk_all_documents()

        print(
            f"Chunks loaded: {len(chunks)}"
        )

        # ----------------------------------------------------
        # Load model
        # ----------------------------------------------------

        model = load_embedding_model()

        # ----------------------------------------------------
        # Create embeddings
        # ----------------------------------------------------

        embeddings = create_embeddings(
            chunks=chunks,
            model=model,
        )

        # ----------------------------------------------------
        # Validate
        # ----------------------------------------------------

        print()

        if validate_embeddings(
            embeddings,
            chunks,
        ):

            print("=" * 70)
            print("SUCCESS: Embedding validation passed.")
            print("=" * 70)

        else:

            print("=" * 70)
            print("ERROR: Embedding validation failed.")
            print("=" * 70)

            raise SystemExit(1)

        # ----------------------------------------------------
        # Test query embedding
        # ----------------------------------------------------

        test_query = (
            "What is the duration of Sannalu rice?"
        )

        print()
        print("Testing query embedding...")
        print(f"Query: {test_query}")

        query_embedding = create_query_embedding(
            test_query,
            model,
        )

        print(
            f"Query vector shape: "
            f"{query_embedding.shape}"
        )

        print()
        print("=" * 70)
        print("SUCCESS: Query embedding test passed.")
        print("=" * 70)

    except Exception as error:

        print()
        print("=" * 70)
        print("ERROR WHILE CREATING EMBEDDINGS")
        print("=" * 70)

        print(error)