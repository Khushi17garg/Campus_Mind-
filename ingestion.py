"""
Member 1 — PDF Processing / Ingestion
CampusMind

Reads PDFs page-by-page, cleans text, splits it into overlapping chunks,
and saves chunk + page/file metadata to JSON.

Expected input:
    data/
        course1/
            notes.pdf
        course2/
            syllabus.pdf

Output:
    processed/chunks.json
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List

try:
    import fitz  # PyMuPDF
except ImportError:
    raise SystemExit("Install PyMuPDF first: pip install pymupdf")


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "processed"
OUTPUT_FILE = OUTPUT_DIR / "chunks.json"

# Adjust these if the team wants larger/smaller chunks.
CHUNK_SIZE = 800          # approximate words per chunk
CHUNK_OVERLAP = 120       # words repeated between adjacent chunks


def clean_text(text: str) -> str:
    """Clean extracted PDF text while keeping useful punctuation."""
    text = text.replace("\x00", " ")
    text = re.sub(r"-\s*\n\s*", "", text)      # join hyphenated line breaks
    text = re.sub(r"\s*\n\s*", " ", text)      # normalize line breaks
    text = re.sub(r"[ \t]+", " ", text)        # repeated spaces
    return text.strip()


def split_into_chunks(text: str, chunk_size: int = CHUNK_SIZE,
                      overlap: int = CHUNK_OVERLAP) -> List[str]:
    """Split text into overlapping word-based chunks."""
    words = text.split()

    if not words:
        return []

    if overlap >= chunk_size:
        raise ValueError("CHUNK_OVERLAP must be smaller than CHUNK_SIZE")

    chunks = []
    step = chunk_size - overlap

    for start in range(0, len(words), step):
        chunk_words = words[start:start + chunk_size]
        if not chunk_words:
            break

        chunks.append(" ".join(chunk_words))

        if start + chunk_size >= len(words):
            break

    return chunks


def process_pdf(pdf_path: Path) -> List[Dict]:
    """Extract page-wise text and create chunks with metadata."""
    records = []

    try:
        document = fitz.open(pdf_path)
    except Exception as exc:
        print(f"Could not open {pdf_path}: {exc}")
        return records

    try:
        for page_number, page in enumerate(document, start=1):
            raw_text = page.get_text("text")
            text = clean_text(raw_text)

            if not text:
                continue

            page_chunks = split_into_chunks(text)

            for chunk_number, chunk in enumerate(page_chunks, start=1):
                records.append(
                    {
                        "chunk_id": (
                            f"{pdf_path.stem}_page_{page_number}"
                            f"_chunk_{chunk_number}"
                        ),
                        "text": chunk,
                        "source": pdf_path.name,
                        "source_path": str(pdf_path.relative_to(BASE_DIR)),
                        "page": page_number,
                        "chunk_number": chunk_number,
                    }
                )
    finally:
        document.close()

    return records


def ingest_all_pdfs() -> List[Dict]:
    """Process every PDF below data/ recursively."""
    pdf_files = sorted(DATA_DIR.rglob("*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in: {DATA_DIR}")
        return []

    all_chunks = []

    for pdf_path in pdf_files:
        print(f"Processing: {pdf_path.relative_to(BASE_DIR)}")
        chunks = process_pdf(pdf_path)
        print(f"  -> {len(chunks)} chunks")
        all_chunks.extend(chunks)

    return all_chunks


def save_chunks(chunks: List[Dict]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    payload = {
        "chunk_count": len(chunks),
        "chunks": chunks,
    }

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)

    print(f"\nSaved {len(chunks)} chunks to: {OUTPUT_FILE}")


if __name__ == "__main__":
    chunks = ingest_all_pdfs()

    if chunks:
        save_chunks(chunks)
    else:
        print("Nothing was saved because no readable PDF text was found.")
