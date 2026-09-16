import os
import json
import sys
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

# Paths Setup
BASE_DIR = os.path.dirname(__file__)
PROCESSED_DIR = os.path.join(BASE_DIR, "processed")
CHUNKS_FILE = os.path.join(PROCESSED_DIR, "chunks.json")
VECTOR_STORE_DIR = os.path.join(BASE_DIR, "vector_store")

# Load Embeddings Model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def load_chunks():
    if not os.path.exists(CHUNKS_FILE):
        raise FileNotFoundError(f"{CHUNKS_FILE} not found. Run ingestion.py first.")
    
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    if isinstance(data, list):
        return data
    return data.get("chunks", [])

def build_vector_store():
    print("🔄 Loading processed text chunks...")
    chunks = load_chunks()
    
    if not chunks:
        print("⚠️ No chunks found to build index.")
        return

    documents = []
    for item in chunks:
        doc = Document(
            page_content=item["text"],
            metadata=item.get("metadata", {})
        )
        documents.append(doc)

    print(f"📦 Generating FAISS embeddings for {len(documents)} chunks...")
    db = FAISS.from_documents(documents, embeddings)
    
    os.makedirs(VECTOR_STORE_DIR, exist_ok=True)
    db.save_local(VECTOR_STORE_DIR)
    print(f"✅ Vector database successfully saved to: {VECTOR_STORE_DIR}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        build_vector_store()
    else:
        build_vector_store()

        
