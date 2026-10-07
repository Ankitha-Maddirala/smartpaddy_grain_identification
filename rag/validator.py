from typing import Optional

from .config import SUPPORTED_VARIETIES


# ============================================================
# SMART PADDY PROJECT - VARIETY VALIDATOR
# ============================================================


def _clean_text(value: str) -> str:
    """
    Normalize user input for comparison.

    Examples:
        "MTU 1010" -> "mtu 1010"
        "  Sannalu  " -> "sannalu"
    """
    if not isinstance(value, str):
        return ""

    value = value.strip().lower()
    value = " ".join(value.split())

    return value


def normalize_variety(variety: str) -> Optional[str]:
    """
    Convert a supported variety name or alias into its
    canonical variety name.

    Returns:
        Canonical variety name if supported.
        None if unsupported or invalid.
    """

    cleaned = _clean_text(variety)

    if not cleaned:
        return None

    for canonical_name, details in SUPPORTED_VARIETIES.items():

        # Check canonical name
        if cleaned == _clean_text(canonical_name):
            return canonical_name

        # Check aliases
        for alias in details.get("aliases", []):
            if cleaned == _clean_text(alias):
                return canonical_name

    return None


def is_supported_variety(variety: str) -> bool:
    """
    Check whether the given variety is one of the
    four supported SMART PADDY varieties.
    """

    return normalize_variety(variety) is not None


def validate_variety(variety: str) -> str:
    """
    Validate a variety.

    Returns:
        Canonical variety name.

    Raises:
        ValueError if the variety is unsupported.
    """

    canonical_name = normalize_variety(variety)

    if canonical_name is None:
        supported_names = ", ".join(SUPPORTED_VARIETIES.keys())

        raise ValueError(
            f"Unsupported paddy variety: '{variety}'. "
            f"Supported varieties are only: {supported_names}."
        )

    return canonical_name


def get_supported_varieties() -> list[str]:
    """
    Return the four supported canonical variety names.
    """

    return list(SUPPORTED_VARIETIES.keys())


def get_variety_aliases(variety: str) -> list[str]:
    """
    Return aliases for a supported variety.
    """

    canonical_name = validate_variety(variety)

    return SUPPORTED_VARIETIES[canonical_name].get(
        "aliases",
        []
    )


def get_variety_document_keywords(variety: str) -> list[str]:
    """
    Return document matching keywords for a supported variety.
    """

    canonical_name = validate_variety(variety)

    return SUPPORTED_VARIETIES[canonical_name].get(
        "document_keywords",
        []
    )


# ============================================================
# TEST FUNCTION
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("SMART PADDY - VARIETY VALIDATOR TEST")
    print("=" * 60)

    test_inputs = [
        "Sannalu",
        "MTU 1010",
        "Cottondora Sannalu",
        "Bondalu",
        "PLA 1100",
        "Badava Mahsuri",
        "RNR 15048",
        "Telangana Sona",
        "Swarna",
        "MTU 7029",
        "BPT 5204",
        "IR 64",
        "",
    ]

    for item in test_inputs:

        try:
            result = validate_variety(item)

            print(
                f"INPUT: {item!r:25} "
                f"-> ACCEPTED: {result}"
            )

        except ValueError:
            print(
                f"INPUT: {item!r:25} "
                f"-> REJECTED"
            )

    print("=" * 60)