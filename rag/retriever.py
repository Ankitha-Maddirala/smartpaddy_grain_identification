"""
SMART PADDY PROJECT
RAG Retriever

Purpose:
    Retrieve relevant knowledge from the FAISS vector store.

Important rule:
    If a variety is selected, retrieval is restricted to:

        Selected variety documents
        +
        Common documents

    Example:

        Sannalu
            -> sannalu_information.docx
            -> common documents

        Bondalu
            -> bondalu_information.docx
            -> common documents

        RNR 15048
            -> rnr_information.docx
            -> common documents

        Swarna
            -> swarna_information.docx
            -> common documents

    Another variety's document must NOT be returned.
"""

from typing import Dict, List

from rag.config import (
    DEFAULT_TOP_K,
    MIN_SIMILARITY_SCORE,
)

from rag.validator import validate_variety

from rag.embeddings import (
    load_embedding_model,
    create_query_embedding,
)

from rag.vector_store import (
    load_faiss_index,
    load_chunks,
    search_index,
)


# ============================================================
# LOAD VECTOR STORE
# ============================================================

def load_retrieval_system():
    """
    Load:

        FAISS index
        Chunks
        Embedding model

    Returns:
        index, chunks, model
    """

    print("Loading FAISS vector index...")

    index = load_faiss_index()

    print(
        f"FAISS vectors loaded: {index.ntotal}"
    )

    print("Loading chunk metadata...")

    chunks = load_chunks()

    print(
        f"Chunks loaded: {len(chunks)}"
    )

    print("Loading embedding model...")

    model = load_embedding_model()

    print("Retrieval system loaded successfully.")

    return index, chunks, model


# ============================================================
# CHECK WHETHER CHUNK IS ALLOWED
# ============================================================

def is_chunk_allowed(
    chunk: Dict,
    selected_variety: str,
) -> bool:
    """
    Decide whether a chunk is allowed for
    the selected variety.

    Allowed:

        selected variety
        common

    Not allowed:

        other varieties
    """

    chunk_variety = chunk.get(
        "variety",
        "",
    )

    return (
        chunk_variety == selected_variety
        or chunk_variety == "common"
    )


# ============================================================
# FILTER SEARCH RESULTS
# ============================================================

def filter_results_by_variety(
    results,
    selected_variety: str,
):
    """
    Remove chunks belonging to other varieties.
    """

    filtered_results = []

    for chunk, score in results:

        if is_chunk_allowed(
            chunk,
            selected_variety,
        ):

            filtered_results.append(
                (
                    chunk,
                    score,
                )
            )

    return filtered_results


# ============================================================
# RETRIEVE KNOWLEDGE
# ============================================================

def retrieve(
    query: str,
    selected_variety: str,
    index,
    chunks: List[Dict],
    model,
    top_k: int = DEFAULT_TOP_K,
    similarity_threshold: float = MIN_SIMILARITY_SCORE,
):
    """
    Retrieve relevant RAG knowledge.

    Parameters:
        query:
            Farmer/user question.

        selected_variety:
            Sannalu
            Bondalu
            RNR 15048
            Swarna

        index:
            FAISS index.

        chunks:
            Stored RAG chunks.

        model:
            Sentence Transformer model.

        top_k:
            Number of final results.

        similarity_threshold:
            Minimum similarity score.
    """

    # --------------------------------------------------------
    # Validate variety
    # --------------------------------------------------------

    selected_variety = validate_variety(
        selected_variety
    )

    # --------------------------------------------------------
    # Validate query
    # --------------------------------------------------------

    if not query or not query.strip():

        raise ValueError(
            "Query cannot be empty."
        )

    # --------------------------------------------------------
    # Create query embedding
    # --------------------------------------------------------

    query_embedding = create_query_embedding(
        query=query,
        model=model,
    )

    # --------------------------------------------------------
    # Search more results than required.
    #
    # Reason:
    # Some top results may belong to another variety.
    # We filter them afterward.
    # --------------------------------------------------------

    search_k = min(
        max(top_k * 5, 20),
        index.ntotal,
    )

    raw_results = search_index(
        query_embedding=query_embedding,
        index=index,
        chunks=chunks,
        top_k=search_k,
    )

    # --------------------------------------------------------
    # Variety filtering
    # --------------------------------------------------------

    filtered_results = filter_results_by_variety(
        results=raw_results,
        selected_variety=selected_variety,
    )

    # --------------------------------------------------------
    # Similarity filtering
    # --------------------------------------------------------

    filtered_results = [
        (
            chunk,
            score,
        )
        for chunk, score in filtered_results
        if score >= similarity_threshold
    ]

    # --------------------------------------------------------
    # Sort by similarity score
    # --------------------------------------------------------

    filtered_results.sort(
        key=lambda item: item[1],
        reverse=True,
    )

    # --------------------------------------------------------
    # Return top K
    # --------------------------------------------------------

    return filtered_results[:top_k]


# ============================================================
# FORMAT RETRIEVED CONTEXT
# ============================================================

def format_retrieved_context(
    results,
) -> str:
    """
    Convert retrieved chunks into a context string
    for the LLM.

    The LLM will later receive this context.
    """

    if not results:

        return (
            "No sufficiently relevant verified "
            "knowledge was retrieved."
        )

    context_parts = []

    for number, (chunk, score) in enumerate(
        results,
        start=1,
    ):

        section = (
            f"[SOURCE {number}]\n"
            f"Source: {chunk['source']}\n"
            f"Variety: {chunk['variety']}\n"
            f"Document Type: {chunk['document_type']}\n"
            f"Similarity Score: {score:.4f}\n"
            f"Content:\n{chunk['text']}"
        )

        context_parts.append(
            section
        )

    return "\n\n".join(
        context_parts
    )


# ============================================================
# PRINT RETRIEVAL RESULTS
# ============================================================

def print_results(
    results,
    selected_variety: str,
    query: str,
):
    """
    Print retrieval results for testing.
    """

    print()
    print("=" * 70)
    print("RAG RETRIEVAL TEST")
    print("=" * 70)

    print()
    print(
        f"Selected Variety : {selected_variety}"
    )

    print(
        f"Query            : {query}"
    )

    print()
    print(
        f"Results returned : {len(results)}"
    )

    print()

    if not results:

        print(
            "No relevant results found."
        )

        return

    for number, (chunk, score) in enumerate(
        results,
        start=1,
    ):

        print("-" * 70)

        print(
            f"Result {number}"
        )

        print(
            f"Score      : {score:.4f}"
        )

        print(
            f"Variety    : {chunk['variety']}"
        )

        print(
            f"Category   : {chunk['category']}"
        )

        print(
            f"Source     : {chunk['source']}"
        )

        print(
            f"Type       : {chunk['document_type']}"
        )

        preview = chunk["text"][:400]

        if len(chunk["text"]) > 400:
            preview += "..."

        print(
            f"Content    : {preview}"
        )

    print("-" * 70)


# ============================================================
# VALIDATE RETRIEVAL SAFETY
# ============================================================

def validate_retrieval_results(
    results,
    selected_variety: str,
) -> bool:
    """
    Make sure retrieval did not return another
    variety's document.
    """

    for chunk, score in results:

        chunk_variety = chunk.get(
            "variety",
            "",
        )

        if chunk_variety not in {
            selected_variety,
            "common",
        }:

            print(
                "ERROR: Retrieval returned "
                "an unauthorized variety!"
            )

            print(
                f"Selected variety: "
                f"{selected_variety}"
            )

            print(
                f"Returned variety: "
                f"{chunk_variety}"
            )

            print(
                f"Source: "
                f"{chunk.get('source')}"
            )

            return False

    return True


# ============================================================
# MAIN TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("SMART PADDY - RAG RETRIEVER TEST")
    print("=" * 70)

    try:

        # ----------------------------------------------------
        # Load retrieval system
        # ----------------------------------------------------

        index, chunks, model = (
            load_retrieval_system()
        )

        # ----------------------------------------------------
        # Test 1: Sannalu
        # ----------------------------------------------------

        selected_variety = "Sannalu"

        query = (
            "What is the duration and yield "
            "of Sannalu rice?"
        )

        results = retrieve(
            query=query,
            selected_variety=selected_variety,
            index=index,
            chunks=chunks,
            model=model,
            top_k=5,
        )

        print_results(
            results=results,
            selected_variety=selected_variety,
            query=query,
        )

        if not validate_retrieval_results(
            results,
            selected_variety,
        ):

            raise RuntimeError(
                "Sannalu retrieval safety test failed."
            )

        # ----------------------------------------------------
        # Test 2: Bondalu
        # ----------------------------------------------------

        selected_variety = "Bondalu"

        query = (
            "What are the important characteristics "
            "of Bondalu rice?"
        )

        results = retrieve(
            query=query,
            selected_variety=selected_variety,
            index=index,
            chunks=chunks,
            model=model,
            top_k=5,
        )

        print_results(
            results=results,
            selected_variety=selected_variety,
            query=query,
        )

        if not validate_retrieval_results(
            results,
            selected_variety,
        ):

            raise RuntimeError(
                "Bondalu retrieval safety test failed."
            )

        # ----------------------------------------------------
        # Test 3: RNR 15048
        # ----------------------------------------------------

        selected_variety = "RNR 15048"

        query = (
            "What are the important features "
            "of RNR 15048?"
        )

        results = retrieve(
            query=query,
            selected_variety=selected_variety,
            index=index,
            chunks=chunks,
            model=model,
            top_k=5,
        )

        print_results(
            results=results,
            selected_variety=selected_variety,
            query=query,
        )

        if not validate_retrieval_results(
            results,
            selected_variety,
        ):

            raise RuntimeError(
                "RNR 15048 retrieval safety test failed."
            )

        # ----------------------------------------------------
        # Test 4: Swarna
        # ----------------------------------------------------

        selected_variety = "Swarna"

        query = (
            "What are the important features "
            "of Swarna rice?"
        )

        results = retrieve(
            query=query,
            selected_variety=selected_variety,
            index=index,
            chunks=chunks,
            model=model,
            top_k=5,
        )

        print_results(
            results=results,
            selected_variety=selected_variety,
            query=query,
        )

        if not validate_retrieval_results(
            results,
            selected_variety,
        ):

            raise RuntimeError(
                "Swarna retrieval safety test failed."
            )

        # ----------------------------------------------------
        # Final success
        # ----------------------------------------------------

        print()
        print("=" * 70)
        print(
            "SUCCESS: RAG retrieval and "
            "variety filtering tests passed."
        )
        print("=" * 70)

    except Exception as error:

        print()
        print("=" * 70)
        print("ERROR WHILE TESTING RAG RETRIEVER")
        print("=" * 70)

        print(error)