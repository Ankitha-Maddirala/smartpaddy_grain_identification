from pathlib import Path
from typing import List, Dict

from pypdf import PdfReader
from docx import Document

from .config import RAG_DOCUMENTS_DIR


# ============================================================
# SMART PADDY PROJECT
# RAG DOCUMENT LOADER
# ============================================================


def read_txt_file(file_path: Path) -> str:
    """
    Read a plain text file.
    """

    return file_path.read_text(
        encoding="utf-8",
        errors="ignore"
    )


def read_pdf_file(file_path: Path) -> str:
    """
    Read all text from a PDF file.
    """

    reader = PdfReader(str(file_path))

    pages = []

    for page in reader.pages:
        try:
            text = page.extract_text()
        except Exception:
            text = ""

        if text:
            pages.append(text)

    return "\n".join(pages)


def read_docx_file(file_path: Path) -> str:
    """
    Read paragraphs and tables from a DOCX file.
    """

    document = Document(str(file_path))

    parts = []

    # --------------------------------------------------------
    # Read normal paragraphs
    # --------------------------------------------------------

    for paragraph in document.paragraphs:

        text = paragraph.text.strip()

        if text:
            parts.append(text)

    # --------------------------------------------------------
    # Read tables
    # --------------------------------------------------------

    for table in document.tables:

        for row in table.rows:

            row_values = []

            for cell in row.cells:

                cell_text = cell.text.strip()

                if cell_text:
                    row_values.append(cell_text)

            if row_values:
                parts.append(" | ".join(row_values))

    return "\n".join(parts)


def load_document(file_path: Path) -> str:
    """
    Load a supported document based on its extension.
    """

    extension = file_path.suffix.lower()

    if extension == ".txt":
        return read_txt_file(file_path)

    if extension == ".pdf":
        return read_pdf_file(file_path)

    if extension == ".docx":
        return read_docx_file(file_path)

    raise ValueError(
        f"Unsupported document format: {file_path.name}"
    )


def clean_text(text: str) -> str:
    """
    Basic text cleaning.

    This does NOT rewrite agricultural information.
    It only removes unnecessary whitespace.
    """

    if not text:
        return ""

    lines = []

    for line in text.splitlines():

        line = " ".join(line.split())

        if line:
            lines.append(line)

    return "\n".join(lines)


def discover_documents() -> List[Path]:
    """
    Find all supported documents inside RAG_DOCUMENTS.
    """

    if not RAG_DOCUMENTS_DIR.exists():

        raise FileNotFoundError(
            f"RAG documents folder not found:\n"
            f"{RAG_DOCUMENTS_DIR}"
        )

    documents = []

    for file_path in sorted(RAG_DOCUMENTS_DIR.iterdir()):

        if not file_path.is_file():
            continue

        if file_path.suffix.lower() in {
            ".docx",
            ".pdf",
            ".txt",
        }:
            documents.append(file_path)

    return documents


def load_all_documents() -> List[Dict]:
    """
    Load all supported documents from RAG_DOCUMENTS.

    Returns a list containing:
        - file_name
        - file_path
        - raw_text
        - cleaned_text
    """

    document_paths = discover_documents()

    loaded_documents = []

    for file_path in document_paths:

        try:
            raw_text = load_document(file_path)

            cleaned = clean_text(raw_text)

            loaded_documents.append(
                {
                    "file_name": file_path.name,
                    "file_path": str(file_path),
                    "raw_text": raw_text,
                    "text": cleaned,
                }
            )

        except Exception as error:

            print(
                f"[WARNING] Could not read "
                f"{file_path.name}: {error}"
            )

    return loaded_documents


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("SMART PADDY - RAG DOCUMENT LOADER TEST")
    print("=" * 70)

    print(f"\nRAG DOCUMENTS FOLDER:")
    print(RAG_DOCUMENTS_DIR)

    print("\nSearching for documents...\n")

    documents = load_all_documents()

    print(f"Documents found: {len(documents)}")
    print("-" * 70)

    for index, document in enumerate(
        documents,
        start=1
    ):

        file_name = document["file_name"]
        text = document["text"]

        print(
            f"{index}. {file_name}"
        )

        print(
            f"   Characters loaded: {len(text):,}"
        )

        if text:

            preview = text[:200].replace(
                "\n",
                " "
            )

            print(
                f"   Preview: {preview}..."
            )

        else:

            print(
                "   WARNING: No text extracted."
            )

        print()

    print("-" * 70)

    if len(documents) == 8:

        print(
            "SUCCESS: All 8 RAG documents were loaded."
        )

    else:

        print(
            f"WARNING: Expected 8 documents, "
            f"but found {len(documents)}."
        )

    print("=" * 70)