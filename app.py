import streamlit as st
import os
import subprocess
from query import generate_answer

st.set_page_config(page_title="Campus Mind - Course Assistant", layout="wide")
st.title("🎓 Campus Mind - RAG Assistant")

# Ensure target course directory exists
DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "ToC")
os.makedirs(DATA_DIR, exist_ok=True)

# Sidebar: File Upload & Index Management
with st.sidebar:
    st.header("⚙️ Document Management")
    
    selected_course = st.selectbox("Select Course", ["ToC", "SPM", "General"])
    
    # PDF Upload Option
    uploaded_files = st.file_uploader("Upload Course PDFs", type=["pdf"], accept_multiple_files=True)
    
    if uploaded_files:
        for file in uploaded_files:
            file_path = os.path.join(DATA_DIR, file.name)
            with open(file_path, "wb") as f:
                f.write(file.getbuffer())
        st.success(f"Uploaded {len(uploaded_files)} PDF(s) to data/ToC/")

    # Rebuild Index Button
    if st.button("🔄 Rebuild Vector Index"):
        with st.spinner("Processing PDFs and rebuilding index..."):
            try:
                subprocess.run(["python", "ingestion.py"], check=True)
                subprocess.run(["python", "vector_store.py", "build"], check=True)
                st.success("Vector database successfully rebuilt!")
            except Exception as e:
                st.error(f"Error rebuilding database: {e}")

# Session State for Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render Previous Chat Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            with st.expander("📚 View Sources"):
                for src in message["sources"]:
                    st.write(f"- **File:** `{src['file']}` | **Page:** {src['page']}")

# Handle User Input
if prompt := st.chat_input("Ask a question about your course materials..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching context and generating answer..."):
            try:
                answer, sources = generate_answer(selected_course, prompt)
                
                # Fallback check if retrieval yields empty response
                if not answer or answer.strip() == "":
                    answer = "I could not find relevant information in the index. Please make sure the vector store is rebuilt."
                
                st.markdown(answer)
                
                if sources:
                    with st.expander("📚 View Sources"):
                        for src in sources:
                            st.write(f"- **File:** `{src['file']}` | **Page:** {src['page']}")
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })
            except Exception as e:
                st.error(f"Error executing query: {e}")
                
