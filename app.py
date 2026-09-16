import streamlit as st
import os
import subprocess
from query import generate_answer

# Page Configuration
st.set_page_config(
    page_title="Campus Mind - AI Tutor", 
    page_icon="🎓", 
    layout="wide"
)

# Custom CSS for Modern UI
st.markdown("""
    <style>
    .main-header {
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .metric-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 12px;
        text-align: center;
        color: #f8fafc;
    }
    .stButton>button {
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# App Header & Metric Cards
st.markdown('<div class="main-header">🎓 Campus Mind - Pro AI Tutor</div>', unsafe_allow_html=True)
st.caption("Offline, Syllabus-Aware Study Assistant powered by Llama 3.1 & FAISS")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="metric-card">⚡ <b>Status:</b> Ready (Local RAG)</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card">🤖 <b>Model:</b> Llama 3.1 8B</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card">🔒 <b>Privacy:</b> 100% Offline</div>', unsafe_allow_html=True)

st.divider()

# Ensure Target Directory
DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "ToC")
os.makedirs(DATA_DIR, exist_ok=True)

# Sidebar - Document Management & Extra Utilities
with st.sidebar:
    st.header("⚙️ Control Panel")
    selected_course = st.selectbox("Select Course", ["ToC", "SPM", "General"])
    
    st.subheader("📤 Document Ingestion")
    uploaded_files = st.file_uploader("Upload Course PDFs", type=["pdf"], accept_multiple_files=True)
    
    if uploaded_files:
        for file in uploaded_files:
            file_path = os.path.join(DATA_DIR, file.name)
            with open(file_path, "wb") as f:
                f.write(file.getbuffer())
        st.success(f"Uploaded {len(uploaded_files)} PDF(s) to system!")

    if st.button("🔄 Rebuild Vector Index", use_container_width=True):
        with st.spinner("Processing documents & updating vector store..."):
            try:
                subprocess.run(["python", "ingestion.py"], check=True)
                subprocess.run(["python", "vector_store.py", "build"], check=True)
                st.success("Vector store synchronized!")
            except Exception as e:
                st.error(f"Failed to rebuild index: {e}")
                
    st.divider()
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Initialize Chat State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Quick Prompt Pills
st.write("💡 **Quick Prompts:**")
p_col1, p_col2, p_col3 = st.columns(3)
prompt_input = None

if p_col1.button("📌 Summarize Unit 1 Notes"):
    prompt_input = "Summarize the key concepts of Unit 1 in bullet points."
if p_col2.button("❓ Generate 3 Practice MCQs"):
    prompt_input = "Generate 3 multiple choice questions with answers based on the uploaded documents."
if p_col3.button("📝 Explain Important Terms"):
    prompt_input = "List and define the most important terms found in the course materials."

# Display Previous Chat Timeline
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            with st.expander("📚 View Cited Sources"):
                for src in message["sources"]:
                    st.info(f"📄 **File:** `{src['file']}` | **Page:** {src['page']}")

# Handle User Input (Chat Box or Quick Prompt)
chat_prompt = st.chat_input("Ask anything from your course materials...")
final_prompt = prompt_input or chat_prompt

if final_prompt:
    st.session_state.messages.append({"role": "user", "content": final_prompt})
    with st.chat_message("user"):
        st.markdown(final_prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching documents & generating response..."):
            try:
                answer, sources = generate_answer(selected_course, final_prompt)
                
                if not answer or answer.strip() == "":
                    answer = "No relevant context found. Please ensure documents are uploaded and the vector index is rebuilt."
                
                st.markdown(answer)
                
                if sources:
                    with st.expander("📚 View Cited Sources"):
                        for src in sources:
                            st.info(f"📄 **File:** `{src['file']}` | **Page:** {src['page']}")
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })
            except Exception as e:
                st.error(f"Error fetching answer: {e}")
                

                
