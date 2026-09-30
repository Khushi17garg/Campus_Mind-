# 🎓 Campus Mind | Enterprise-Grade, 100% Offline AI Tutor & Assessment System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-121212?style=for-the-badge&logo=chainlink&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-black?style=for-the-badge)
![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-00599C?style=for-the-badge)

**Campus Mind** is a privacy-first, fully local Retrieval-Augmented Generation (RAG) platform designed for academic study, concept verification, and automated self-assessment. Built entirely for local CPU execution, it guarantees **100% data privacy** with zero external cloud dependencies while offering verifiable page-cited answers, interactive practice exams, and smart flashcard generation.

---

## 🌟 Key Features & Capabilities

* **🔒 100% Offline & Privacy-First Architecture:** Operates entirely on local hardware using Ollama (`llama3.2:3b`) and FAISS vector indices. No API keys, no monthly costs, and complete data isolation.
* **📚 Verifiable Page-Level Citations:** Eliminates LLM hallucinations by tagging every generated response, practice quiz item, and flashcard with exact page references (`File Name`, `Page Number`).
* **🎯 Interactive Assessment Center (MCQ Engine):** Generates structured multiple-choice questions with dual assessment modes:
  * **3-Question Specific Focus:** Targeted practice on specific pages or sub-topics.
  * **10-Question Comprehensive Exam:** Full document mastery check.
* **🎴 Smart Study Flashcards:** Automatically extracts high-yield definitions, core formulas, and key concepts into clean, expandable memory cards.
* **⚡ CPU-Optimized RAG Pipeline:** Leverages lightweight embeddings (`sentence-transformers/all-MiniLM-L6-v2`) and 600-character chunking to deliver fast response times on standard consumer laptops.

---

## 🛠️ Tech Stack & Dependencies

| Layer | Tool / Framework | Function |
| :--- | :--- | :--- |
| **Frontend UI** | Streamlit | Multi-tab interactive web dashboard |
| **Local LLM Engine** | Ollama (`llama3.2:3b`) | Task execution, quiz synthesis & response generation |
| **Orchestration** | LangChain | RAG pipeline, prompt engineering, and retriever mechanics |
| **Vector Database** | FAISS | High-speed local similarity search and indexing |
| **Embeddings** | HuggingFace (`all-MiniLM-L6-v2`) | Lightweight 384-dimensional text embeddings |
| **Document Processing** | PyPDF Directory Loader | Local PDF loading, parsing, and chunking |

---

## 📁 Project Directory Structure

```text
Campus_Mind/
├── data/                  # Storage directory for uploaded course PDFs
├── vector_store/          # Saved FAISS index and binary metadata
├── app.py                 # Core Streamlit multi-tab user application
├── query.py               # RAG retrieval and context augmentation pipeline
├── quiz_engine.py         # MCQ generation engine with JSON sanitization
├── flashcards.py          # Flashcard deck extractor with regex fallback
├── ingestion.py           # Document chunking & recursive splitting setup
├── vector_store.py        # Local vector database creation & search setup
└── requirements.txt       # Python project dependencies

🚀 Quick Setup & Installation
1. System Requirements
Python: 3.10 or higher

Ollama: Installed locally (Download Ollama)

2. Prepare Local LLM
Open your terminal and pull the optimized local Llama model:
ollama pull llama3.2:3b
3. Clone Repository & Install Dependencies
Bash
git clone [https://github.com/Khushi17garg/Campus_Mind-.git](https://github.com/Khushi17garg/Campus_Mind-.git)
cd Campus_Mind-
pip install -r requirements.txt
4. Run Application
Start the Streamlit application server:
python -m streamlit run app.py
💡 How to Use Campus Mind
Document Ingestion: Upload course PDFs via the left sidebar control panel.

Build Index: Click 🔄 Rebuild Vector Index to parse materials into the FAISS vector database.

💬 AI Chat Tutor: Ask questions, request summaries, or click quick prompt buttons to query course materials.

🎯 Assessment Center: Select quiz scope (3 or 10 questions), attempt MCQs, and submit for instant performance analysis and explanations.

🎴 Smart Flashcards: Enter an optional topic focus or leave blank to extract core study cards across the whole material.

