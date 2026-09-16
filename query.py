import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

# Load Embeddings & LLM
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
llm = Ollama(model="llama3.1:8b")

VECTOR_STORE_PATH = os.path.join(os.path.dirname(__file__), "vector_store")

def generate_answer(course_name: str, query: str):
    """
    Generates answer and retrieves citations based on user query intent.
    """
    # Safety check: ensure query is a valid string
    if not query:
        return "Please enter a valid prompt or select a quick option.", []

    if not os.path.exists(VECTOR_STORE_PATH):
        return "Vector database not found. Please upload PDFs and rebuild the index.", []

    # Load FAISS index
    db = FAISS.load_local(VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True)
    
    # Safe query checks for intent-based dynamic k-value
    query_str = str(query).lower()
    is_broad_request = any(keyword in query_str for keyword in ["summarize", "summary", "mcq", "quiz", "terms", "key concepts"])
    k_value = 8 if is_broad_request else 4

    retriever = db.as_retriever(search_kwargs={"k": k_value})

    template = """You are CampusMind, an expert AI tutor for university courses.
Use the following pieces of retrieved context from course materials to answer the question.

If the user asks for:
- A summary: Provide a structured, well-organized overview in bullet points.
- MCQs or Quiz: Generate clear multiple-choice questions with 4 options (A, B, C, D) and specify the correct answer at the end.
- Definitions/Terms: Provide clean, concise definitions based on the context.

Retrieved Context:
{context}

User Question: {question}

Detailed Answer:"""

    prompt = PromptTemplate(template=template, input_variables=["context", "question"])

    docs = retriever.invoke(query)
    context_text = "\n\n".join([doc.page_content for doc in docs])
    formatted_prompt = prompt.format(context=context_text, question=query)

    response = llm.invoke(formatted_prompt)

    sources = []
    for doc in docs:
        meta = doc.metadata
        sources.append({
            "file": meta.get("source", "Unknown PDF"),
            "page": meta.get("page", "N/A")
        })

    unique_sources = []
    seen = set()
    for s in sources:
        identifier = (s["file"], s["page"])
        if identifier not in seen:
            seen.add(identifier)
            unique_sources.append(s)

    return response, unique_sources






