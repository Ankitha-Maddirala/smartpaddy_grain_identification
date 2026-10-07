"""
SMART PADDY PROJECT
RAG Cultivation Planner

Purpose:
    Prepare verified RAG context for the cultivation planner.

Inputs:
    - Grain variety
    - Land size

Supported varieties:
    - Sannalu
    - Bondalu
    - RNR 15048
    - Swarna

Land sizes:
    - 1 Acre
    - 2 Acres
    - 3 Acres
    - Custom

Important rule:
    This module does NOT invent agricultural values.

    Quantities are scaled only when the retrieved source
    provides a valid base quantity and scaling is explicitly
    possible.

    If a value is not available in the verified documents,
    the planner must say that the verified documents do
    not provide that value.
"""

from typing import Dict, List, Any

from rag.validator import validate_variety

from rag.retriever import (
    load_retrieval_system,
    retrieve,
    format_retrieved_context,
)


# ============================================================
# SUPPORTED LAND SIZES
# ============================================================

STANDARD_LAND_SIZES = {
    "1 Acre": 1.0,
    "2 Acres": 2.0,
    "3 Acres": 3.0,
}


# ============================================================
# NORMALIZE LAND SIZE
# ============================================================

def normalize_land_size(
    land_size: Any,
) -> Dict[str, Any]:
    """
    Convert land-size input into a standard structure.

    Examples:

        "1 Acre"
        "2 Acres"
        "3 Acres"
        1
        2
        3

    Custom numeric values are also accepted.
    """

    if land_size is None:

        raise ValueError(
            "Land size is required."
        )

    # --------------------------------------------------------
    # String input
    # --------------------------------------------------------

    if isinstance(
        land_size,
        str,
    ):

        cleaned = (
            land_size
            .strip()
            .lower()
        )

        # Standard options
        if cleaned in {
            "1 acre",
            "1",
            "1.0",
        }:

            return {
                "label": "1 Acre",
                "acres": 1.0,
                "is_standard": True,
            }

        if cleaned in {
            "2 acres",
            "2 acre",
            "2",
            "2.0",
        }:

            return {
                "label": "2 Acres",
                "acres": 2.0,
                "is_standard": True,
            }

        if cleaned in {
            "3 acres",
            "3 acre",
            "3",
            "3.0",
        }:

            return {
                "label": "3 Acres",
                "acres": 3.0,
                "is_standard": True,
            }

        # Try custom numeric input
        try:

            acres = float(
                cleaned.replace(
                    "acres",
                    "",
                )
                .replace(
                    "acre",
                    "",
                )
                .strip()
            )

        except ValueError:

            raise ValueError(
                "Invalid land size. "
                "Enter a positive number of acres."
            )

    # --------------------------------------------------------
    # Numeric input
    # --------------------------------------------------------

    elif isinstance(
        land_size,
        (int, float),
    ):

        acres = float(
            land_size
        )

    else:

        raise ValueError(
            "Invalid land size type."
        )

    # --------------------------------------------------------
    # Validate numeric value
    # --------------------------------------------------------

    if acres <= 0:

        raise ValueError(
            "Land size must be greater than 0 acres."
        )

    # --------------------------------------------------------
    # Standard/custom label
    # --------------------------------------------------------

    if acres == 1.0:

        label = "1 Acre"
        is_standard = True

    elif acres == 2.0:

        label = "2 Acres"
        is_standard = True

    elif acres == 3.0:

        label = "3 Acres"
        is_standard = True

    else:

        label = f"{acres:g} Acres"
        is_standard = False

    return {
        "label": label,
        "acres": acres,
        "is_standard": is_standard,
    }


# ============================================================
# PLANNER RETRIEVAL QUERIES
# ============================================================

def build_planner_queries(
    selected_variety: str,
) -> List[str]:
    """
    Create retrieval queries covering the main areas
    required by the cultivation planner.

    These are retrieval questions, NOT invented answers.
    """

    selected_variety = validate_variety(
        selected_variety
    )

    queries = [

        # Variety information
        (
            f"What are the important characteristics, "
            f"duration, yield, season, adaptability, "
            f"grain characteristics and resistance "
            f"information for {selected_variety}?"
        ),

        # Land and soil
        (
            f"What soil, land preparation and field "
            f"requirements are documented for "
            f"{selected_variety} rice cultivation?"
        ),

        # Seed / nursery / planting
        (
            f"What verified information is available "
            f"about seed, nursery, transplanting, "
            f"spacing and establishment for "
            f"{selected_variety}?"
        ),

        # Water
        (
            f"What water management, irrigation and "
            f"drainage practices are recommended in "
            f"the verified documents for "
            f"{selected_variety}?"
        ),

        # Nutrients
        (
            f"What fertilizer, nutrient management and "
            f"deficiency information is available for "
            f"{selected_variety}?"
        ),

        # Pest and disease
        (
            f"What pest, disease and weed management "
            f"information is relevant to "
            f"{selected_variety} rice?"
        ),

        # Harvest
        (
            f"What harvesting, drying and storage "
            f"information is documented for "
            f"{selected_variety} rice?"
        ),
    ]

    return queries


# ============================================================
# RETRIEVE PLANNER KNOWLEDGE
# ============================================================

def retrieve_planner_knowledge(
    selected_variety: str,
    index,
    chunks: List[Dict],
    model,
    per_query_top_k: int = 4,
) -> List[Dict]:
    """
    Retrieve verified knowledge for all planner topics.

    Duplicate chunks are removed.
    """

    selected_variety = validate_variety(
        selected_variety
    )

    queries = build_planner_queries(
        selected_variety
    )

    collected = {}

    for query in queries:

        results = retrieve(
            query=query,
            selected_variety=selected_variety,
            index=index,
            chunks=chunks,
            model=model,
            top_k=per_query_top_k,
        )

        for chunk, score in results:

            chunk_id = chunk["chunk_id"]

            # Keep highest score if the same chunk
            # appears in multiple query results.
            if (
                chunk_id not in collected
                or score > collected[chunk_id]["score"]
            ):

                collected[chunk_id] = {
                    "chunk": chunk,
                    "score": score,
                    "query": query,
                }

    # --------------------------------------------------------
    # Sort by relevance
    # --------------------------------------------------------

    sorted_results = sorted(
        collected.values(),
        key=lambda item: item["score"],
        reverse=True,
    )

    return sorted_results


# ============================================================
# BUILD PLANNER CONTEXT
# ============================================================

def build_planner_context(
    selected_variety: str,
    land_size: Any,
    index,
    chunks: List[Dict],
    model,
) -> Dict:
    """
    Prepare the complete verified context that will later
    be passed to the LLM.
    """

    selected_variety = validate_variety(
        selected_variety
    )

    land = normalize_land_size(
        land_size
    )

    knowledge = retrieve_planner_knowledge(
        selected_variety=selected_variety,
        index=index,
        chunks=chunks,
        model=model,
    )

    # --------------------------------------------------------
    # Convert retrieval results to the format expected
    # by the context builder.
    # --------------------------------------------------------

    retrieval_results = [
        (
            item["chunk"],
            item["score"],
        )
        for item in knowledge
    ]

    context_text = format_retrieved_context(
        retrieval_results
    )

    # --------------------------------------------------------
    # Planner instructions
    # --------------------------------------------------------

    planner_rules = """
PLANNER RULES

1. Use only information supported by the retrieved
   verified RAG documents.

2. Do not invent fertilizer rates, seed rates, water
   quantities, labour requirements, yields, costs,
   pesticide doses or other numerical values.

3. If a required value is not present in the verified
   documents, explicitly say:
   "The verified documents do not provide this value."

4. Do not use information belonging to another rice variety.

5. Common rice cultivation, water management, pest/disease/
   weed management and fertilizer/nutrient documents may be
   used as supporting knowledge.

6. Variety-specific information has priority when available.

7. Land size is context. Do not automatically multiply a
   quantity unless the source provides a valid base quantity
   and scaling is scientifically/arithmetically justified.

8. Experimental or study-specific values must be clearly
   labelled as experimental/study-specific.

9. Do not treat Swarna-Sub1 as the same variety as normal
   Swarna.

10. If the retrieved evidence is insufficient, clearly say
    that the verified RAG knowledge base does not provide
    enough information instead of guessing.
""".strip()

    return {
        "selected_variety": selected_variety,
        "land_size": land,
        "retrieved_chunks": knowledge,
        "context_text": context_text,
        "planner_rules": planner_rules,
    }


# ============================================================
# BUILD LLM PROMPT
# ============================================================

def build_planner_prompt(
    planner_context: Dict,
) -> str:
    """
    Build the prompt that will later be sent to an LLM.

    This function only creates the prompt.
    It does not call an external LLM.
    """

    selected_variety = (
        planner_context["selected_variety"]
    )

    land = planner_context["land_size"]

    context_text = (
        planner_context["context_text"]
    )

    planner_rules = (
        planner_context["planner_rules"]
    )

    prompt = f"""
You are the Smart Paddy Cultivation Planner.

Selected rice variety:
{selected_variety}

Land size:
{land['label']} ({land['acres']} acres)

You must prepare a practical cultivation plan using
ONLY the verified RAG context supplied below.

IMPORTANT:
Do not invent missing agricultural information.

{planner_rules}

Prepare the plan using this structure:

1. Selected Variety
2. Land Size
3. Variety Overview
4. Suitable Season / Growing Duration
5. Soil and Field Preparation
6. Seed / Nursery / Establishment
7. Spacing and Planting
8. Water Management
9. Nutrient / Fertilizer Management
10. Weed Management
11. Pest and Disease Management
12. Crop Growth-Stage Management
13. Harvesting
14. Drying and Storage
15. Important Precautions
16. Information Not Available in Verified Documents

For every numerical value, make sure it is supported
by the retrieved documents.

If a value is unavailable, say so explicitly.

VERIFIED RAG CONTEXT
====================

{context_text}
""".strip()

    return prompt


# ============================================================
# PRINT PLANNER SUMMARY
# ============================================================

def print_planner_summary(
    planner_context: Dict,
) -> None:
    """
    Print planner retrieval information.
    """

    selected_variety = (
        planner_context["selected_variety"]
    )

    land = planner_context["land_size"]

    retrieved_chunks = (
        planner_context["retrieved_chunks"]
    )

    print()
    print("=" * 70)
    print("SMART PADDY - CULTIVATION PLANNER TEST")
    print("=" * 70)

    print()
    print(
        f"Selected Variety : {selected_variety}"
    )

    print(
        f"Land Size        : {land['label']}"
    )

    print(
        f"Acres            : {land['acres']}"
    )

    print(
        f"Standard Size    : {land['is_standard']}"
    )

    print()
    print(
        f"Retrieved chunks : "
        f"{len(retrieved_chunks)}"
    )

    print()
    print("TOP RETRIEVED KNOWLEDGE")
    print("-" * 70)

    for number, item in enumerate(
        retrieved_chunks[:10],
        start=1,
    ):

        chunk = item["chunk"]
        score = item["score"]

        print()
        print(
            f"{number}. Score: {score:.4f}"
        )

        print(
            f"   Variety: "
            f"{chunk['variety']}"
        )

        print(
            f"   Source: "
            f"{chunk['source']}"
        )

        preview = chunk["text"][:250]

        if len(chunk["text"]) > 250:
            preview += "..."

        print(
            f"   Text: {preview}"
        )


# ============================================================
# MAIN TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("SMART PADDY - CULTIVATION PLANNER TEST")
    print("=" * 70)

    try:

        # ----------------------------------------------------
        # Load RAG retrieval system
        # ----------------------------------------------------

        index, chunks, model = (
            load_retrieval_system()
        )

        # ----------------------------------------------------
        # Test planner
        # ----------------------------------------------------

        selected_variety = "Sannalu"
        land_size = "2 Acres"

        planner_context = build_planner_context(
            selected_variety=selected_variety,
            land_size=land_size,
            index=index,
            chunks=chunks,
            model=model,
        )

        # ----------------------------------------------------
        # Print summary
        # ----------------------------------------------------

        print_planner_summary(
            planner_context
        )

        # ----------------------------------------------------
        # Build prompt
        # ----------------------------------------------------

        prompt = build_planner_prompt(
            planner_context
        )

        print()
        print("=" * 70)
        print("LLM PROMPT PREVIEW")
        print("=" * 70)

        print()

        # Print only first 3000 characters
        # so terminal output stays manageable.
        print(
            prompt[:3000]
        )

        if len(prompt) > 3000:

            print()
            print(
                "... prompt preview truncated ..."
            )

        # ----------------------------------------------------
        # Final success
        # ----------------------------------------------------

        print()
        print("=" * 70)
        print(
            "SUCCESS: Cultivation planner "
            "context and prompt created."
        )
        print("=" * 70)

    except Exception as error:

        print()
        print("=" * 70)
        print(
            "ERROR WHILE BUILDING "
            "CULTIVATION PLANNER"
        )
        print("=" * 70)

        print(error)