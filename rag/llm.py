"""
SMART PADDY
API-Key-Free LLM Layer

Temporary version for project development/demo.

This version does NOT require:
- OpenAI API key
- Internet
- Paid API

It converts the verified RAG context into a structured
cultivation plan.

Later, if Sir asks for an actual LLM API, only this layer
needs to be replaced. RAG, documents, retrieval and UI
can remain unchanged.
"""

from typing import Optional

from .validator import validate_variety


# ============================================================
# VARIETY VALIDATION
# ============================================================

def validate_selected_variety(selected_variety: str) -> str:
    """
    Validate and normalize the selected paddy variety.
    """

    return validate_variety(selected_variety)


# ============================================================
# LAND SIZE
# ============================================================

def validate_land_size(land_size: str) -> str:
    """
    Validate land-size input.
    """

    if land_size is None:
        raise ValueError("Land size is required.")

    land_size = str(land_size).strip()

    if not land_size:
        raise ValueError("Land size cannot be empty.")

    # Standard UI options
    allowed = {
        "1 Acre",
        "2 Acres",
        "3 Acres",
    }

    if land_size in allowed:
        return land_size

    # Custom numeric value
    try:
        value = float(
            land_size
            .lower()
            .replace("acres", "")
            .replace("acre", "")
            .strip()
        )

        if value <= 0:
            raise ValueError

        return f"{value:g} Acres"

    except ValueError:
        raise ValueError(
            "Invalid land size. Use 1 Acre, 2 Acres, "
            "3 Acres, or a positive custom value."
        )


# ============================================================
# TEXT EXTRACTION HELPERS
# ============================================================

def _clean_text(text: str) -> str:
    """
    Clean unnecessary whitespace.
    """

    if not text:
        return ""

    lines = []

    for line in str(text).splitlines():

        line = line.strip()

        if line:
            lines.append(line)

    return "\n".join(lines)


def _limit_text(text: str, max_chars: int = 5000) -> str:
    """
    Keep generated demo output manageable.
    """

    text = _clean_text(text)

    if len(text) <= max_chars:
        return text

    return text[:max_chars].rstrip() + "\n..."


# ============================================================
# RAG CONTEXT PARSER
# ============================================================

def extract_context_sections(rag_context: str) -> list[str]:
    """
    Convert retrieved RAG context into readable sections.

    This does NOT create new agricultural facts.
    It only organizes retrieved information.
    """

    if not rag_context:
        return []

    context = _clean_text(rag_context)

    sections = []

    current = []

    for line in context.splitlines():

        line = line.strip()

        if not line:
            continue

        # Common section/document separators
        if (
            line.startswith("SOURCE:")
            or line.startswith("DOCUMENT:")
            or line.startswith("VARIETY:")
            or line.startswith("SECTION:")
            or line.startswith("CHUNK:")
        ):

            if current:
                sections.append("\n".join(current))
                current = []

        current.append(line)

    if current:
        sections.append("\n".join(current))

    return sections


# ============================================================
# BUILD KNOWLEDGE-BASED PLAN
# ============================================================

def build_cultivation_plan(
    selected_variety: str,
    land_size: str,
    rag_context: str,
) -> str:
    """
    Build a structured cultivation plan from retrieved RAG context.

    IMPORTANT:
    This temporary version does not invent agricultural values.

    It presents retrieved knowledge under structured headings.
    """

    variety = validate_selected_variety(selected_variety)
    land = validate_land_size(land_size)

    context = _clean_text(rag_context)

    if not context:
        return (
            "No verified RAG information was retrieved for this "
            "cultivation plan."
        )

    sections = extract_context_sections(context)

    # --------------------------------------------------------
    # Build structured response
    # --------------------------------------------------------

    plan_parts = []

    plan_parts.append(
        f"# Cultivation Plan — {variety}"
    )

    plan_parts.append(
        f"**Land Size:** {land}"
    )

    plan_parts.append(
        "\n## Important Note\n"
        "This plan is generated from the verified Smart Paddy "
        "RAG knowledge base. Values that are not available in "
        "the retrieved documents are not invented."
    )

    plan_parts.append(
        "\n## 1. Variety Information"
    )

    plan_parts.append(
        "The following verified information was retrieved "
        "for the selected variety:"
    )

    # First relevant retrieved information
    if sections:

        variety_information = "\n\n".join(
            sections[:3]
        )

        plan_parts.append(
            _limit_text(variety_information, 6000)
        )

    else:

        plan_parts.append(
            context[:6000]
        )

    plan_parts.append(
        "\n## 2. Cultivation Guidance"
    )

    plan_parts.append(
        "Use the retrieved RAG information below for field "
        "preparation, establishment, water, nutrients, "
        "weed management, pest and disease management, "
        "and harvesting."
    )

    if len(sections) > 3:

        cultivation_information = "\n\n".join(
            sections[3:]
        )

        plan_parts.append(
            _limit_text(cultivation_information, 10000)
        )

    else:

        plan_parts.append(
            _limit_text(context, 10000)
        )

    plan_parts.append(
        "\n## 3. Land-Size Consideration"
    )

    plan_parts.append(
        f"The selected land size is **{land}**."
    )

    plan_parts.append(
        "Quantities are scaled only when a verified base "
        "quantity is available in the RAG documents. "
        "Otherwise, the value should be treated as "
        "not available from the verified documents."
    )

    plan_parts.append(
        "\n## 4. Important Precautions"
    )

    plan_parts.append(
        "- Follow variety-specific recommendations where available."
    )

    plan_parts.append(
        "- Do not substitute information from another rice variety."
    )

    plan_parts.append(
        "- Do not assume fertilizer, pesticide, water, seed, "
        "labour or yield quantities that are not present "
        "in the verified documents."
    )

    plan_parts.append(
        "- Experimental or study-specific values must be "
        "treated as experimental, not universal recommendations."
    )

    plan_parts.append(
        "\n## 5. Information Not Available"
    )

    plan_parts.append(
        "If a required agricultural quantity or recommendation "
        "is not present in the verified RAG documents, it is "
        "not generated or guessed by this system."
    )

    return "\n\n".join(plan_parts)


# ============================================================
# COMPATIBILITY FUNCTION
# ============================================================

def generate_llm_response(
    prompt: str,
    model: Optional[str] = None,
    temperature: float = 0.2,
) -> str:
    """
    Temporary compatibility function.

    The previous implementation called OpenAI.
    This version does NOT call an external API.

    The prompt is returned as structured knowledge text.
    """

    if not prompt or not prompt.strip():
        raise ValueError("Prompt is empty.")

    return (
        "RAG-based response prepared successfully.\n\n"
        + prompt.strip()
    )


# ============================================================
# PLANNER COMPATIBILITY FUNCTION
# ============================================================

def generate_cultivation_plan(
    planner_prompt: str,
    selected_variety: str,
    land_size: str,
    model: Optional[str] = None,
) -> str:
    """
    Compatibility wrapper.

    Later this function can be replaced with an actual LLM call
    without changing the planner/UI architecture.
    """

    variety = validate_selected_variety(selected_variety)
    land = validate_land_size(land_size)

    return (
        f"# Cultivation Plan — {variety}\n\n"
        f"**Land Size:** {land}\n\n"
        "## RAG-Based Cultivation Information\n\n"
        f"{planner_prompt.strip()}\n\n"
        "## Important\n\n"
        "This temporary API-key-free version uses the verified "
        "RAG information directly. No unsupported agricultural "
        "values have been generated."
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("SMART PADDY - API-KEY-FREE LLM LAYER TEST")
    print("=" * 70)

    test_variety = "Sannalu"
    test_land = "2 Acres"

    try:

        variety = validate_selected_variety(test_variety)
        land = validate_land_size(test_land)

        print(f"\nSelected Variety : {variety}")
        print(f"Land Size        : {land}")

        test_context = """
SOURCE: sannalu_information.docx
VARIETY: Sannalu - MTU 1010

Sannalu is also known as Cottondora Sannalu and MTU 1010.
It is a rice variety suitable for Andhra Pradesh and Telangana.

SOURCE: COMMON RICE CULTIVATION.docx

Rice cultivation includes field preparation, nursery or
establishment, water management, nutrient management,
weed management, pest and disease management and harvesting.

SOURCE: WATER MANAGEMENT.docx

Water management should be based on crop stage, soil,
rainfall and field conditions.
"""

        result = build_cultivation_plan(
            selected_variety=variety,
            land_size=land,
            rag_context=test_context,
        )

        print("\n" + "=" * 70)
        print("GENERATED PLAN")
        print("=" * 70)

        print(result)

        print("\n" + "=" * 70)
        print("SUCCESS: API-key-free LLM layer test completed.")
        print("=" * 70)

    except Exception as e:

        print("\n" + "=" * 70)
        print("TEST FAILED")
        print("=" * 70)

        print(type(e).__name__ + ":", e)