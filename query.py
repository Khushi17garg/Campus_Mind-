import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

# Paths and model definitions
VECTOR_STORE_PATH = os.path.join(os.path.dirname(__file__), "vector_store")
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "llama3.1:8b"

def generate_answer(course_name: str, question: str):
    # Load vector store and embeddings
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    
    if not os.path.exists(VECTOR_STORE_PATH):
        return "Vector store not found. Please run vector_store.py build first.", []

    vector_store = FAISS.load_local(
        VECTOR_STORE_PATH, 
        embeddings, 
        allow_dangerous_deserialization=True
    )
    
    # Retrieve top relevant documents
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    retrieved_docs = retriever.invoke(question)
    
    if not retrieved_docs:
        return "I could not find this information in the uploaded course documents.", []

    # Combine text context from documents
    context_text = "\n\n".join([doc.page_content for doc in retrieved_docs])
    
    # Define prompt template
    template = """
    You are an assistant for answering questions based on course materials.
    Use the following context to answer the question. If the answer cannot be found in the context, say "I could not find this information in the uploaded course documents."

    Context:
    {context}

    Question: {question}

    Answer:
    """
    
    prompt = PromptTemplate(template=template, input_variables=["context", "question"])
    llm = Ollama(model=LLM_MODEL)
    
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
    sample_question = "What is Software Project Management?"

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




