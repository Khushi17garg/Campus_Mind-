import os
from langchain_community.document_loaders import PyPDFDirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_and_split_documents(data_dir: str):
    """
    Loads all PDFs from the given course directory and splits them into optimized chunks.
    """
    if not os.path.exists(data_dir):
        print(f"Directory {data_dir} does not exist.")
        return []

    print(f"Loading PDFs from: {data_dir}")
    loader = PyPDFDirectoryLoader(data_dir)
    documents = loader.load()

    if not documents:
        print("No documents found to process.")
        return []

    # Optimized smaller chunk sizes (600 characters) for faster embedding generation on CPU
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=60,
        length_function=len,
        is_separator_regex=False,
    )

    chunks = text_splitter.split_documents(documents)
    print(f"Successfully processed {len(documents)} document pages into {len(chunks)} chunks.")
    return chunks

if __name__ == "__main__":
    # Test run standalone
    base_data_path = os.path.join(os.path.dirname(__file__), "data")
    chunks = load_and_split_documents(base_data_path)

    