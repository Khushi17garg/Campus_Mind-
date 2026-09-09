"""
Member 2 — Embeddings + FAISS
CampusMind

Reads processed/chunks.json created by ingestion.py, converts each chunk
to a sentence embedding, builds a FAISS index, and provides retrieval.

Outputs:
    vector_store/index.faiss
    vector_store/metadata.json

Usage:
    python vector_store.py build
    python vector_store.py search "What is compiler design?"
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

try:
    import faiss
except ImportError:
    raise SystemExit("Install FAISS first: pip install faiss-cpu")

try:
    import numpy as np
except ImportError:
    raise SystemExit("Install NumPy first: pip install numpy")

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    raise SystemExit(
        "Install sentence-transformers first: "
        "pip install sentence-transformers"
    )


BASE_DIR = Path(__file__).resolve().parent
CHUNKS_FILE = BASE_DIR / "processed" / "chunks.json"
STORE_DIR = BASE_DIR / "vector_store"
INDEX_FILE = STORE_DIR / "index.faiss"
METADATA_FILE = STORE_DIR / "metadata.json"

# Lightweight and good for a student RAG project.
MODEL_NAME = "all-MiniLM-L6-v2"


def load_chunks() -> List[Dict]:
    """Load chunk records produced by ingestion.py."""
    if not CHUNKS_FILE.exists():
        raise FileNotFoundError(
            f"{CHUNKS_FILE} not found. Run ingestion.py first."
        )

    with CHUNKS_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    chunks = data.get("chunks", [])
    if not chunks:
        raise ValueError("chunks.json contains no chunks.")

    return chunks


def get_model() -> SentenceTransformer:
    """Load the embedding model."""
    print(f"Loading embedding model: {MODEL_NAME}")
    return SentenceTransformer(MODEL_NAME)


def build_index() -> None:
    """Create and save a normalized FAISS cosine-similarity index."""
    chunks = load_chunks()
    texts = [item["text"] for item in chunks]

    model = get_model()
    print(f"Creating embeddings for {len(texts)} chunks...")

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True,
        normalize_embeddings=True,
    ).astype("float32")

    dimension = embeddings.shape[1]

    # Inner product on normalized vectors = cosine similarity.
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    STORE_DIR.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(INDEX_FILE))

    metadata = {
        "model": MODEL_NAME,
        "dimension": dimension,
        "count": len(chunks),
        "chunks": chunks,
    }

    with METADATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(metadata, file, ensure_ascii=False, indent=2)

    print(f"\nFAISS index saved to: {INDEX_FILE}")
    print(f"Metadata saved to: {METADATA_FILE}")


def load_index() -> Tuple[faiss.Index, List[Dict], SentenceTransformer]:
    """Load an existing index, metadata, and embedding model."""
    if not INDEX_FILE.exists() or not METADATA_FILE.exists():
        raise FileNotFoundError(
            "FAISS index not found. Run: python vector_store.py build"
        )

    index = faiss.read_index(str(INDEX_FILE))

    with METADATA_FILE.open("r", encoding="utf-8") as file:
        metadata = json.load(file)

    chunks = metadata["chunks"]
    model = get_model()

    return index, chunks, model


def retrieve(query: str, top_k: int = 5) -> List[Dict]:
    """Return the most relevant chunks for a question."""
    if not query.strip():
        return []

    index, chunks, model = load_index()

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True,
    ).astype("float32")

    top_k = min(max(1, top_k), len(chunks))
    scores, indices = index.search(query_embedding, top_k)

    results = []

    for score, index_number in zip(scores[0], indices[0]):
        if index_number < 0:
            continue

        item = dict(chunks[index_number])
        item["score"] = float(score)
        results.append(item)

    return results


def print_results(results: List[Dict]) -> None:
    """Print retrieved chunks in a readable format."""
    if not results:
        print("No results found.")
        return

    for number, item in enumerate(results, start=1):
        print("\n" + "=" * 70)
        print(f"Result {number} | similarity: {item['score']:.4f}")
        print(f"Source: {item['source']} | Page: {item['page']}")
        print("-" * 70)
        print(item["text"])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Commands:")
        print("  python vector_store.py build")
        print('  python vector_store.py search "your question"')
        raise SystemExit(1)

    command = sys.argv[1].lower()

    if command == "build":
        build_index()

    elif command == "search":
        if len(sys.argv) < 3:
            raise SystemExit('Example: python vector_store.py search "What is AI?"')

        question = " ".join(sys.argv[2:])
        results = retrieve(question, top_k=5)
        print_results(results)

    else:
        raise SystemExit(f"Unknown command: {command}")
