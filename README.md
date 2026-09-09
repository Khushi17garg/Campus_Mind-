# CampusMind 🎓

CampusMind is an offline, syllabus-aware AI tutor for college students. It helps students ask questions from their own academic PDFs—such as syllabus documents, unit notes, and previous-year question papers—and provides answers with the relevant document name and page number.

The project uses Retrieval-Augmented Generation (RAG), vector search, and a local Large Language Model (LLM), so it can work without paid cloud APIs.

---

## Problem Statement

Students often have many PDFs containing notes, course syllabi, and previous-year question papers. Finding a correct answer or a topic across all these files takes time.

CampusMind solves this problem by allowing students to upload course PDFs and ask questions in simple language. The system searches the uploaded documents, retrieves relevant content, and generates a source-based answer.

---

## Features

- Upload and manage course PDFs
- Supports notes, syllabus files, and previous-year question papers
- Course-wise document organization
- Natural-language question answering
- Retrieval-Augmented Generation (RAG)
- Source citations with PDF filename and page number
- Local vector search using FAISS
- Offline local LLM support through Ollama
- Simple and student-friendly Streamlit interface
- No paid API key required

---

## How It Works

CampusMind follows this workflow:

```text
PDFs → Text Extraction → Chunking → Embeddings → FAISS Vector Database
                                                      ↓
Student Question → Similarity Search → Relevant Chunks → Local LLM → Answer + Sources
```

1. The user uploads PDFs for a selected course.
2. CampusMind extracts text from every PDF page.
3. The text is split into small chunks with metadata such as course name, file name, and page number.
4. Each chunk is converted into a numerical embedding.
5. Embeddings are stored in a FAISS vector database.
6. When a student asks a question, the system retrieves the most relevant chunks.
7. A local LLM uses only the retrieved context to generate an answer.
8. The answer is displayed along with the source PDF name and page number.

---

## Technology Stack

| Category | Technology |
|---|---|
| Programming Language | Python |
| User Interface | Streamlit |
| RAG Framework | LangChain |
| PDF Text Extraction | PyPDF / pdfplumber |
| Embedding Model | Sentence Transformers |
| Vector Database | FAISS |
| Local LLM | Ollama |
| Suggested LLM Models | Llama 3.1 / Mistral |
| Version Control | Git and GitHub |

---

## Project Structure

```text
campusmind/
│
├── app.py                  # Streamlit user interface
├── ingestion.py            # PDF extraction, chunking, embeddings, FAISS index creation
├── query.py                # Retrieval and LLM question-answering logic
├── config.py               # Application configuration
├── requirements.txt        # Python dependencies
├── README.md
│
├── data/                   # Course PDFs
│   ├── ToC/
│   ├── CN/
│   └── DBMS/
│
└── indexes/                # Generated FAISS indexes
    ├── ToC/
    ├── CN/
    └── DBMS/
```

---

## Installation

### Prerequisites

Install the following before running the project:

- Python 3.10 or above
- Git
- Ollama

Verify Python and Git installation:

```bash
python --version
git --version
```

---

### 1. Clone the Repository

```bash
git clone [https://github.com/YOUR-GITHUB-USERNAME/campusmind.git](https://github.com/YOUR-GITHUB-USERNAME/campusmind.git)
cd campusmind
```

Replace `YOUR-GITHUB-USERNAME` with your GitHub username.

---

### 2. Create and Activate a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

If the `requirements.txt` file is not available yet, install the basic dependencies using:

```bash
pip install streamlit langchain langchain-community langchain-ollama sentence-transformers faiss-cpu pypdf pdfplumber python-dotenv
```

---

### 4. Install a Local LLM

Install Ollama from [ollama.com](https://ollama.com).

Then download a model:

```bash
ollama pull llama3.1:8b
```

Check installed models:

```bash
ollama list
```

---

### 5. Add Course PDFs

Place course PDFs inside the appropriate course folder:

```text
data/
├── ToC/
│   ├── syllabus.pdf
│   ├── unit1_notes.pdf
│   └── previous_year_questions.pdf
│
├── CN/
│   ├── syllabus.pdf
│   └── unit_notes.pdf
```

---

### 6. Create the Vector Index

Run the ingestion script for each course:

```bash
python ingestion.py --course ToC --data_path data/ToC
```

Example for Computer Networks:

```bash
python ingestion.py --course CN --data_path data/CN
```

The generated FAISS index will be saved inside the `indexes/` directory.

---

### 7. Run CampusMind

```bash
streamlit run app.py
```

Open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

---

## Example Questions

- What is a Turing Machine? Explain with an example.
- Explain the difference between a PDA and a Turing Machine.
- List the important topics from Unit 2.
- What are the applications of context-free grammar?
- Explain CSMA/CD in simple words.
- Give important previous-year questions from Unit 3.

---

## Team Responsibilities

| Team Member | Responsibility |
|---|---|
| Member 1 | PDF extraction, metadata handling, and text chunking |
| Member 2 | Embedding generation, FAISS vector database, and retrieval |
| Member 3| Local LLM integration, prompt engineering, and RAG pipeline |
| Member 4 | Streamlit UI, testing, screenshots, documentation, and presentation |

> Replace “Member 1–4” with your team members’ actual names.

---

## Future Enhancements

- Multi-turn conversation history
- Support for DOCX, PPTX, and image-based PDFs
- OCR for scanned PDF notes
- Voice-based question input
- Answer export to PDF
- Quiz generation from uploaded notes
- Automatic revision planner
- Deployment on a college server
- Role-based login for students and teachers

---

## License

This project is developed for academic and educational purposes.

---

## Contributors

- Khushi Garg
- Vedika singh
- Ayushi singh
- Yamini
