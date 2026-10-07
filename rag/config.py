from pathlib import Path


# ============================================================
# SMART PADDY PROJECT - RAG CONFIGURATION
# ============================================================

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# RAG documents folder
RAG_DOCUMENTS_DIR = PROJECT_ROOT / "RAG_DOCUMENTS"

# RAG generated data
RAG_DATA_DIR = PROJECT_ROOT / "rag_data"

# Vector index
VECTOR_INDEX_DIR = RAG_DATA_DIR / "faiss_index"

# Metadata file
METADATA_FILE = RAG_DATA_DIR / "metadata.json"

# Supported varieties
SUPPORTED_VARIETIES = {
    "Sannalu": {
        "canonical_name": "Sannalu",
        "aliases": [
            "sannalu",
            "mtu 1010",
            "mtu1010",
            "cottondora sannalu",
            "cottondora sannalu mtu 1010",
        ],
        "document_keywords": [
            "sannalu",
            "mtu1010",
            "mtu 1010",
        ],
    },

    "Bondalu": {
        "canonical_name": "Bondalu",
        "aliases": [
            "bondalu",
            "pla 1100",
            "pla1100",
            "badava mahsuri",
            "badava mahshuri",
        ],
        "document_keywords": [
            "bondalu",
            "pla1100",
            "pla 1100",
        ],
    },

    "RNR 15048": {
        "canonical_name": "RNR 15048",
        "aliases": [
            "rnr 15048",
            "rnr15048",
            "telangana sona",
            "telangana sona rnr 15048",
        ],
        "document_keywords": [
            "rnr",
            "rnr15048",
            "telangana sona",
        ],
    },

    "Swarna": {
        "canonical_name": "Swarna",
        "aliases": [
            "swarna",
            "mtu 7029",
            "mtu7029",
            "swarna mtu 7029",
        ],
        "document_keywords": [
            "swarna",
            "mtu7029",
            "mtu 7029",
        ],
    },
}


# Common documents.
COMMON_DOCUMENT_KEYWORDS = {
    "common_rice": [
        "common",
        "rice cultivation",
    ],

    "water_management": [
        "water",
        "management",
        "irrigation",
    ],

    "pest_disease": [
        "pest",
        "disease",
        "weed",
    ],

    "fertilizer_nutrient": [
        "fertilizer",
        "nutrient",
    ],
}


# Embedding model
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


# Retrieval settings
DEFAULT_TOP_K = 8

# Minimum similarity score.
# This is a retrieval control, NOT a factual confidence score.
MIN_SIMILARITY_SCORE = 0.25


# Chunk settings
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200


# Supported document extensions
SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
}