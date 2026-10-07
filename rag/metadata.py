"""
SMART PADDY PROJECT
RAG Metadata Builder

Purpose:
    Assign metadata to every RAG document.

Supported varieties:
    - Sannalu
    - Bondalu
    - RNR 15048
    - Swarna

Common documents:
    - Common Rice Cultivation
    - Water Management
    - Pest / Disease / Weed Management
    - Fertilizer / Nutrient Management
"""

from pathlib import Path
from typing import Dict, List

from rag.document_loader import load_all_documents


# ============================================================
# VARIETY DOCUMENT MAPPING
# ============================================================

VARIETY_DOCUMENT_MAP = {
    "sannalu_information.docx": "Sannalu",
    "bondalu_information.docx": "Bondalu",
    "rnr_information.docx": "RNR 15048",
    "swarna_information.docx": "Swarna",
}


# ============================================================
# COMMON DOCUMENT MAPPING
# ============================================================

COMMON_DOCUMENT_MAP = {
    "COMMON RICE CULTIVATION.docx": "common",
    "WATER MANAGEMENT.docx": "common",
    "PEST.docx": "common",
    "FERTILIZER.docx": "common",
}


# ============================================================
# DOCUMENT TYPE MAPPING
# ============================================================

DOCUMENT_TYPE_MAP = {
    "sannalu_information.docx": "variety_information",
    "bondalu_information.docx": "variety_information",
    "rnr_information.docx": "variety_information",
    "swarna_information.docx": "variety_information",

    "COMMON RICE CULTIVATION.docx": "common_rice_cultivation",
    "WATER MANAGEMENT.docx": "water_management",
    "PEST.docx": "pest_disease_weed_management",
    "FERTILIZER.docx": "fertilizer_nutrient_management",
}


# ============================================================
# CATEGORY MAPPING
# ============================================================

CATEGORY_MAP = {
    "sannalu_information.docx": "variety",
    "bondalu_information.docx": "variety",
    "rnr_information.docx": "variety",
    "swarna_information.docx": "variety",

    "COMMON RICE CULTIVATION.docx": "common",
    "WATER MANAGEMENT.docx": "common",
    "PEST.docx": "common",
    "FERTILIZER.docx": "common",
}


# ============================================================
# NORMALIZE FILE NAME
# ============================================================

def normalize_filename(filename: str) -> str:
    """
    Normalize filename for reliable matching.
    """

    return Path(filename).name.strip().lower()


# ============================================================
# GET DOCUMENT VARIETY
# ============================================================

def get_document_variety(filename: str) -> str:
    """
    Return the variety associated with a document.

    Variety documents:
        Sannalu
        Bondalu
        RNR 15048
        Swarna

    Common documents:
        common
    """

    normalized = normalize_filename(filename)

    for file_name, variety in VARIETY_DOCUMENT_MAP.items():

        if normalized == file_name.lower():
            return variety

    for file_name, variety in COMMON_DOCUMENT_MAP.items():

        if normalized == file_name.lower():
            return variety

    raise ValueError(
        f"Unknown RAG document: {filename}"
    )


# ============================================================
# GET DOCUMENT TYPE
# ============================================================

def get_document_type(filename: str) -> str:
    """
    Return the document type.
    """

    normalized = normalize_filename(filename)

    for file_name, document_type in DOCUMENT_TYPE_MAP.items():

        if normalized == file_name.lower():
            return document_type

    raise ValueError(
        f"Unknown document type for: {filename}"
    )


# ============================================================
# GET DOCUMENT CATEGORY
# ============================================================

def get_document_category(filename: str) -> str:
    """
    Return either:
        variety
        common
    """

    normalized = normalize_filename(filename)

    for file_name, category in CATEGORY_MAP.items():

        if normalized == file_name.lower():
            return category

    raise ValueError(
        f"Unknown document category for: {filename}"
    )


# ============================================================
# BUILD METADATA FOR ONE DOCUMENT
# ============================================================

def build_document_metadata(document: Dict) -> Dict:
    """
    Add metadata fields to one loaded document.
    """

    file_name = document["file_name"]

    variety = get_document_variety(file_name)
    document_type = get_document_type(file_name)
    category = get_document_category(file_name)

    metadata = {
        "file_name": file_name,
        "file_path": document["file_path"],
        "variety": variety,
        "category": category,
        "document_type": document_type,
        "source": file_name,
    }

    return metadata


# ============================================================
# BUILD METADATA FOR ALL DOCUMENTS
# ============================================================

def build_all_metadata() -> List[Dict]:
    """
    Load all RAG documents and create metadata records.
    """

    documents = load_all_documents()

    metadata_records = []

    for document in documents:

        metadata = build_document_metadata(document)

        metadata_records.append(metadata)

    return metadata_records


# ============================================================
# VALIDATE METADATA
# ============================================================

def validate_metadata(metadata_records: List[Dict]) -> bool:
    """
    Validate that all expected documents are present
    and correctly classified.
    """

    # --------------------------------------------------------
    # IMPORTANT:
    # Normalize expected filenames also.
    # This avoids uppercase/lowercase mismatch.
    # --------------------------------------------------------

    expected_files = {
        normalize_filename(file_name)
        for file_name in (
            list(VARIETY_DOCUMENT_MAP.keys())
            + list(COMMON_DOCUMENT_MAP.keys())
        )
    }

    actual_files = {
        normalize_filename(record["file_name"])
        for record in metadata_records
    }

    # --------------------------------------------------------
    # Check missing documents
    # --------------------------------------------------------

    missing = expected_files - actual_files

    if missing:

        print("ERROR: Missing documents:")

        for file_name in sorted(missing):

            print(f"  - {file_name}")

        return False

    # --------------------------------------------------------
    # Check unexpected documents
    # --------------------------------------------------------

    unexpected = actual_files - expected_files

    if unexpected:

        print("WARNING: Unexpected documents found:")

        for file_name in sorted(unexpected):

            print(f"  - {file_name}")

    # --------------------------------------------------------
    # Check valid variety names
    # --------------------------------------------------------

    valid_varieties = {
        "Sannalu",
        "Bondalu",
        "RNR 15048",
        "Swarna",
        "common",
    }

    for record in metadata_records:

        variety = record["variety"]

        if variety not in valid_varieties:

            print(
                f"ERROR: Invalid variety '{variety}' "
                f"in {record['file_name']}"
            )

            return False

    return True


# ============================================================
# PRINT METADATA
# ============================================================

def print_metadata(metadata_records: List[Dict]) -> None:
    """
    Display metadata in a readable format.
    """

    print()
    print("=" * 70)
    print("SMART PADDY - RAG METADATA TEST")
    print("=" * 70)

    print()
    print(f"Documents processed: {len(metadata_records)}")

    print()

    for index, record in enumerate(metadata_records, start=1):

        print(f"{index}. {record['file_name']}")

        print(
            f"   Variety      : {record['variety']}"
        )

        print(
            f"   Category     : {record['category']}"
        )

        print(
            f"   Document Type: {record['document_type']}"
        )

        print(
            f"   Source       : {record['source']}"
        )

        print()


# ============================================================
# MAIN TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("SMART PADDY - RAG METADATA BUILDER TEST")
    print("=" * 70)

    try:

        metadata_records = build_all_metadata()

        print_metadata(metadata_records)

        if validate_metadata(metadata_records):

            print("=" * 70)
            print("SUCCESS: Metadata validation passed.")
            print("=" * 70)

        else:

            print("=" * 70)
            print("ERROR: Metadata validation failed.")
            print("=" * 70)

    except Exception as error:

        print()
        print("=" * 70)
        print("ERROR WHILE BUILDING METADATA")
        print("=" * 70)

        print(error)