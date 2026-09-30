import os
import sys
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from ingestion import load_and_split_documents

# System Paths
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
VECTOR_STORE_DIR = os.path.join(BASE_DIR, "vector_store")

# Lightweight embedding model optimized for local CPU execution (384 dimensions)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)

def build_vector_store():
    """
    Reads PDFs from the data folder and builds/overwrites the local FAISS index.
    """
    print("Starting vector store construction...")
    chunks = load_and_split_documents(DATA_DIR)
    
    if not chunks:
        print("No document chunks available. Vector store build aborted.")
        return False

    print("Embedding chunks into FAISS vector space...")
    vector_db = FAISS.from_documents(chunks, embeddings)
    
    os.makedirs(VECTOR_STORE_DIR, exist_ok=True)
    vector_db.save_local(VECTOR_STORE_DIR)
    print(f"FAISS index successfully saved to: {VECTOR_STORE_DIR}")
    return True

def load_vector_store():
    """
    Loads the saved local FAISS index.
    """
    if os.path.exists(VECTOR_STORE_DIR):
        return FAISS.load_local(VECTOR_STORE_DIR, embeddings, allow_dangerous_deserialization=True)
    print("No existing FAISS vector store found.")
    return None

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        build_vector_store()
    else:
        print("Usage: python vector_store.py build")
        

        
