from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Try importing from Member 2's vector_store; fallback to dummy if not ready yet
try:
    from vector_store import retrieve_context
except (ImportError, ModuleNotFoundError):
    def retrieve_context(course_name: str, question: str):
        return []

LLM_MODEL = "llama3.1:8b"

RAG_PROMPT_TEMPLATE = """
You are CampusMind, a helpful and friendly college AI tutor.
Use ONLY the provided context below to answer the student's question.
If the answer cannot be found in the context, strictly state:
"I could not find this information in the uploaded course documents."

Context:
{context}

Question: {question}

Answer:
"""

def generate_answer(course_name: str, question: str):
    """Retrieves course context and generates an answer using Ollama."""
    retrieved_docs = retrieve_context(course_name, question)
    
    context_text = "\n\n".join([doc.page_content for doc in retrieved_docs]) if retrieved_docs else "No context available."
    
    prompt = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
    llm = OllamaLLM(model=LLM_MODEL)
    
    chain = prompt | llm
    raw_answer = chain.invoke({"context": context_text, "question": question})
    
    sources = []
    for doc in retrieved_docs:
        sources.append({
            "file": doc.metadata.get("filename", "Unknown Document"),
            "page": doc.metadata.get("page", "Unknown Page")
        })
        
    return raw_answer, sources

if __name__ == "__main__":
    sample_course = "ToC"
    sample_question = "What is a Turing Machine?"
    
    print(f"Testing RAG query for course '{sample_course}'...")
    try:
        answer, sources = generate_answer(sample_course, sample_question)
        print("\n--- Answer ---")
        print(answer)
        print("\n--- Sources ---")
        for src in sources:
            print(f"File: {src['file']} | Page: {src['page']}")
    except Exception as e:
        print(f"Error during testing: {e}")
        


