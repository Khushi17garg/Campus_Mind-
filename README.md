🎓 CampusMind - Offline Syllabus-Aware AI Tutor
CampusMind is an offline, syllabus-aware Retrieval-Augmented Generation (RAG) system built to answer student queries using course materials (lecture notes, syllabi, and previous year questions) with exact page-level source citations.

🌟 Key Features
100% Local & Privacy-First: Powered by Ollama (llama3.1:8b) and local embeddings (all-MiniLM-L6-v2), requiring no external API keys or cloud dependencies.

Source Transparency: Every generated answer includes verifiable citations linking back to the precise PDF file and page number.

Interactive Frontend: Built with Streamlit, providing real-time chat interactions and multi-PDF document upload functionality.

Dynamic Indexing: Automatically chunks, processes, and updates vector stores via FAISS.
🏗️ Tech Stack
Language: Python

LLM Engine: Ollama (llama3.1:8b)

Framework: LangChain (langchain-core, langchain-community, langchain-huggingface)

Embeddings: HuggingFace sentence-transformers/all-MiniLM-L6-v2

Vector Store: FAISS

Frontend: Streamlit
Project Structure
Campus_Mind/
│
├── data/                    # PDF storage organized by course modules (e.g., ToC, SPM)
├── processed/               # Contains chunks.json generated during PDF ingestion
├── vector_store/            # Stores FAISS index files (index.faiss, index.pkl)
│
├── ingestion.py             # Parses PDFs and breaks text into structured chunks
├── vector_store.py          # Generates and manages the FAISS vector database
├── query.py                 # Core RAG logic (retrieval + LLM chain generation)
├── app.py                   # Streamlit UI with file uploader and chat timeline
│
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
🚀 Quickstart Guide
1. Prerequisites
Ensure you have Python 3.10+ and Ollama installed locally. Pull the required Llama model:
ollama pull llama3.1:8b
2. Installation
Clone the repository and install the dependencies:

Bash
git clone https://github.com/Khushi17garg/Campus_Mind.git
cd Campus_Mind
pip install -r requirements.txt
3. Running the Pipeline via CLI
If you want to run and test the backend pipeline directly from the terminal:

Ingest Documents:

Bash
python ingestion.py
Build Vector Database:

Bash
python vector_store.py build
Run RAG Query Test:

Bash
python query.py
💻 Running the Web Application
Launch the Streamlit interface:

Bash
streamlit run app.py
Open your browser at http://localhost:8501.

Use the Sidebar to upload course PDFs to the target directory.

Click 🔄 Rebuild Vector Index to synchronize the FAISS database.

Type your question in the chat bar to receive grounded answers with collapsible citations.

