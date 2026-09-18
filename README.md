# 🎓 Campus Mind: Offline Intelligent Academic Tutor

**Campus Mind** is a high-performance, 100% offline Retrieval-Augmented Generation (RAG) platform designed to act as an AI tutor for university students. Powered by Streamlit, LangChain, FAISS, and Ollama, it enables students to query course materials, generate structured unit summaries, build practice MCQs, and extract page-accurate citations without sending data to external APIs.

---

## ✨ Key Features

* **Intent-Aware Context Retrieval:** Dynamically scales retrieval context depth ($k=8$ for broad tasks like summaries and practice quizzes; $k=4$ for specific queries) to ensure comprehensive answers without overwhelming local models.
* **Page-Accurate Citations:** Extracts precise PDF metadata (`source_file` and `page_number`) during ingestion to display transparent source citations under each answer.
* **Optimized Local Generation:** Integrated with `llama3.2:3b` via Ollama for fast, low-latency local inference on standard CPU setups.
* **Interactive Quick Prompts:** Single-click UI shortcuts for generating unit summaries, practice MCQs, and core definitions.
* **Clean, Functional Interface:** A responsive Streamlit frontend featuring course-level filtering, document ingestion tools, and chat management.

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **RAG Framework:** LangChain (`langchain-community`, `langchain-huggingface`, `langchain-core`)
* **Vector Database:** FAISS
* **Embeddings:** HuggingFace (`sentence-transformers/all-MiniLM-L6-v2`)
* **LLM Engine:** Ollama (`llama3.2:3b`)

---

## 📂 Project Structure

```text
Campus_Mind/
│
├── data/                    # Directory for raw course PDFs (e.g., ToC, SPM)
├── processed/               # Contains extracted text chunks and metadata (chunks.json)
├── vector_store/            # Persisted FAISS vector index files
│
├── app.py                   # Streamlit UI & interactive chat execution
├── ingestion.py             # PDF loading, splitting (800/150 overlap), & metadata extraction
├── query.py                 # Intent-aware retrieval logic & Ollama prompt processing
├── vector_store.py          # Script for building/saving FAISS embeddings
├── requirements.txt         # Python project dependencies
└── README.md                # Project documentation
