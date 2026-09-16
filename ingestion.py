import os
import json
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "processed")
OUTPUT_FILE = os.path.join(PROCESSED_DIR, "chunks.json")

def process_documents():
    """
    Loads all PDFs across subdirectories in data/, splits them into chunks, 
    and saves text with clean metadata (source file & page) to JSON.
    """
    if not os.path.exists(DATA_DIR):
        print(f"Error: {DATA_DIR} directory does not exist.")
        return

    os.makedirs(PROCESSED_DIR, exist_ok=True)

    print("📄 Loading PDF files...")
    loader = PyPDFDirectoryLoader(DATA_DIR)
    documents = loader.load()

    if not documents:
        print("⚠️ No PDF documents found in data/ folder!")
        return

    print(f"Loaded {len(documents)} raw pages.")

    # Split documents into optimal chunks for RAG
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        length_function=len
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} text chunks.")

    # Extract structured metadata for exact page-level citations
    processed_chunks = []
    for chunk in chunks:
        file_path = chunk.metadata.get("source", "")
        file_name = os.path.basename(file_path) if file_path else "Unknown File"
        page_num = chunk.metadata.get("page", 0) + 1  # 1-indexed page number

        processed_chunks.append({
            "text": chunk.page_content,
            "metadata": {
                "source": file_name,
                "page": page_num
            }
        })

    # Save processed chunks
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(processed_chunks, f, indent=4, ensure_ascii=False)

    print(f"✅ Successfully processed and saved {len(processed_chunks)} chunks to {OUTPUT_FILE}")

if __name__ == "__main__":
    process_documents()
    

