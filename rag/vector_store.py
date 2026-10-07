"""
SMART PADDY PROJECT
RAG FAISS Vector Store

Purpose:
    Create and save a FAISS vector index from RAG embeddings.

Saved files:
    rag_data/faiss_index/index.faiss
    rag_data/faiss_index/chunks.json
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple

import faiss
import numpy as np

from rag.config import (
    VECTOR_INDEX_DIR,
)
from rag.chunking import chunk_all_documents
from rag.embeddings import (
    load_embedding_model,
    create_embeddings,
)


# ============================================================
# FILE PATHS
# ============================================================

INDEX_FILE = VECTOR_INDEX_DIR / "index.faiss"
CHUNKS_FILE = VECTOR_INDEX_DIR / "chunks.json"


# ============================================================
# CREATE VECTOR INDEX
# ============================================================

def create_faiss_index(
    embeddings: np.ndarray,
) -> faiss.Index:
    """
    Create a FAISS inner-product index.

    Embeddings are normalized, so inner product
    corresponds to cosine similarity.
    """

    if embeddings is None:
        raise ValueError(
            "Embeddings cannot be None."
        )

    if embeddings.ndim != 2:
        raise ValueError(
            "Embeddings must be a 2D NumPy array."
        )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(
        embeddings.astype("float32")
    )

    return index


# ============================================================
# SAVE FAISS INDEX
# ============================================================

def save_faiss_index(
    index: faiss.Index,
    path: Path = INDEX_FILE,
) -> None:
    """
    Save FAISS index to disk.
    """

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    faiss.write_index(
        index,
        str(path),
    )


# ============================================================
# SAVE CHUNKS
# ============================================================

def save_chunks(
    chunks: List[Dict],
    path: Path = CHUNKS_FILE,
) -> None:
    """
    Save chunk metadata/text to JSON.
    """

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        path,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            chunks,
            file,
            ensure_ascii=False,
            indent=2,
        )


# ============================================================
# LOAD FAISS INDEX
# ============================================================

def load_faiss_index(
    path: Path = INDEX_FILE,
) -> faiss.Index:
    """
    Load an existing FAISS index.
    """

    if not path.exists():

        raise FileNotFoundError(
            f"FAISS index not found: {path}"
        )

    return faiss.read_index(
        str(path)
    )


# ============================================================
# LOAD CHUNKS
# ============================================================

def load_chunks(
    path: Path = CHUNKS_FILE,
) -> List[Dict]:
    """
    Load saved chunk metadata/text.
    """

    if not path.exists():

        raise FileNotFoundError(
            f"Chunks file not found: {path}"
        )

    with open(
        path,
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)


# ============================================================
# SEARCH VECTOR INDEX
# ============================================================

def search_index(
    query_embedding: np.ndarray,
    index: faiss.Index,
    chunks: List[Dict],
    top_k: int = 5,
) -> List[Tuple[Dict, float]]:
    """
    Search the FAISS index.

    Returns:
        [(chunk, similarity_score), ...]
    """

    if query_embedding.ndim == 1:

        query_embedding = query_embedding.reshape(
            1,
            -1,
        )

    query_embedding = query_embedding.astype(
        "float32"
    )

    top_k = min(
        top_k,
        index.ntotal,
    )

    scores, indices = index.search(
        query_embedding,
        top_k,
    )

    results = []

    for score, idx in zip(
        scores[0],
        indices[0],
    ):

        if idx < 0:
            continue

        if idx >= len(chunks):
            continue

        results.append(
            (
                chunks[idx],
                float(score),
            )
        )

    return results


# ============================================================
# VALIDATE INDEX
# ============================================================

def validate_index(
    index: faiss.Index,
    chunks: List[Dict],
    embeddings: np.ndarray,
) -> bool:
    """
    Validate that FAISS index and chunks match.
    """

    if index is None:

        print("ERROR: FAISS index is None.")

        return False

    if index.ntotal != len(chunks):

        print(
            "ERROR: FAISS index size does not "
            "match number of chunks."
        )

        print(
            f"FAISS vectors : {index.ntotal}"
        )

        print(
            f"Chunks        : {len(chunks)}"
        )

        return False

    if index.d != embeddings.shape[1]:

        print(
            "ERROR: FAISS dimension does not "
            "match embedding dimension."
        )

        return False

    return True


# ============================================================
# BUILD COMPLETE VECTOR STORE
# ============================================================

def build_vector_store():
    """
    Complete pipeline:

        Documents
            ↓
        Chunks
            ↓
        Embeddings
            ↓
        FAISS Index
            ↓
        Save Index + Chunks
    """

    print()
    print("Loading RAG documents and creating chunks...")

    chunks = chunk_all_documents()

    print(
        f"Total chunks: {len(chunks)}"
    )

    print()
    print("Loading embedding model...")

    model = load_embedding_model()

    print()
    print("Creating embeddings...")

    embeddings = create_embeddings(
        chunks=chunks,
        model=model,
    )

    print()
    print("Creating FAISS index...")

    index = create_faiss_index(
        embeddings
    )

    print(
        f"FAISS vectors: {index.ntotal}"
    )

    print()
    print("Validating vector store...")

    if not validate_index(
        index,
        chunks,
        embeddings,
    ):

        raise RuntimeError(
            "Vector store validation failed."
        )

    print()
    print("Saving FAISS index...")

    save_faiss_index(
        index
    )

    print(
        f"Saved: {INDEX_FILE}"
    )

    print()
    print("Saving chunks...")

    save_chunks(
        chunks
    )

    print(
        f"Saved: {CHUNKS_FILE}"
    )

    return index, chunks, model


# ============================================================
# MAIN TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("SMART PADDY - FAISS VECTOR STORE TEST")
    print("=" * 70)

    try:

        index, chunks, model = build_vector_store()

        # ----------------------------------------------------
        # Test retrieval
        # ----------------------------------------------------

        test_query = (
            "What is the duration of Sannalu rice?"
        )

        print()
        print("=" * 70)
        print("TESTING VECTOR SEARCH")
        print("=" * 70)

        print()
        print(f"Query: {test_query}")

        from rag.embeddings import create_query_embedding

        query_embedding = create_query_embedding(
            test_query,
            model,
        )

        results = search_index(
            query_embedding=query_embedding,
            index=index,
            chunks=chunks,
            top_k=5,
        )

        print()
        print("Top search results:")

        for number, (chunk, score) in enumerate(
            results,
            start=1,
        ):

            print()
            print(
                f"{number}. "
                f"Score: {score:.4f}"
            )

            print(
                f"   Variety: "
                f"{chunk['variety']}"
            )

            print(
                f"   Source: "
                f"{chunk['file_name']}"
            )

            preview = chunk["text"][:250]

            if len(chunk["text"]) > 250:
                preview += "..."

            print(
                f"   Text: {preview}"
            )

        # ----------------------------------------------------
        # Final success
        # ----------------------------------------------------

        print()
        print("=" * 70)
        print("SUCCESS: FAISS vector store created and tested.")
        print("=" * 70)

    except Exception as error:

        print()
        print("=" * 70)
        print("ERROR WHILE BUILDING VECTOR STORE")
        print("=" * 70)

        print(error)