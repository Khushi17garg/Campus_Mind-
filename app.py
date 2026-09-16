import streamlit as st
import os
import subprocess
from query import generate_answer

# --- Page Setup ---
st.set_page_config(
    page_title="Campus Mind | Offline AI Tutor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
    <style>
    .main .block-container {
        padding-top: 2rem;
        max-width: 1000px;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 500;
    }
    div[data-testid="stChatMessage"] {
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.title("🎓 Campus Mind")
st.caption("Your Offline Intelligent Tutor for Academic Materials")

# Ensure Data Directories Exist
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

# --- Sidebar Controls ---
with st.sidebar:
    st.header("⚙️ Control Panel")
    
    selected_course = st.selectbox(
        "Select Course", 
        ["General", "ToC", "SPM"],
        index=0
    )
    
    st.divider()
    st.subheader("🤖 Document Ingestion")
    uploaded_files = st.file_uploader(
        "Upload Course PDFs", 
        type=["pdf"], 
        accept_multiple_files=True
    )
    
    if uploaded_files:
        specific_data_dir = os.path.join(DATA_DIR, selected_course if selected_course != "General" else "")
        os.makedirs(specific_data_dir, exist_ok=True)
        for file in uploaded_files:
            file_path = os.path.join(specific_data_dir, file.name)
            with open(file_path, "wb") as f:
                f.write(file.getbuffer())
        st.success(f"Uploaded {len(uploaded_files)} PDF(s) to system!")

    if st.button("🔄 Rebuild Vector Index", use_container_width=True):
        with st.spinner("Rebuilding knowledge base..."):
            try:
                subprocess.run(["python", "ingestion.py"], check=True)
                subprocess.run(["python", "vector_store.py", "build"], check=True)
                st.success("Vector index successfully rebuilt!")
            except Exception as e:
                st.error(f"Failed to rebuild index: {e}")
                
    st.divider()
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- Initialize Chat State ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Quick Prompts Bar ---
st.write("📍 **Quick Prompts:**")
prompt_input = None
col1, col2, col3 = st.columns(3)

if col1.button("📌 Summarize Unit 1 Notes", use_container_width=True):
    prompt_input = "Summarize the core concepts of Unit 1 in bullet points."
if col2.button("❓ Generate 3 Practice MCQs", use_container_width=True):
    prompt_input = "Generate 3 multiple-choice practice questions (MCQs) with options and key answers based on the material."
if col3.button("📝 Explain Important Terms", use_container_width=True):
    prompt_input = "List and define the key academic terms and definitions from the context."

# --- Render Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            with st.expander("📚 View Cited Sources"):
                for src in message["sources"]:
                    st.info(f"📄 **File:** `{src['file']}` | **Page:** {src['page']}")

# --- Handle User Query & Response Generation ---
chat_prompt = st.chat_input("Ask anything from your course materials...")
final_prompt = prompt_input or chat_prompt

if final_prompt and final_prompt.strip():
    # Save & display user message
    st.session_state.messages.append({"role": "user", "content": final_prompt})
    with st.chat_message("user"):
        st.markdown(final_prompt)

    # Process and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing course material..."):
            try:
                answer, sources = generate_answer(selected_course, final_prompt)
                
                st.markdown(answer)
                
                if sources:
                    with st.expander("📚 View Cited Sources"):
                        for src in sources:
                            st.info(f"📄 **File:** `{src['file']}` | **Page:** {src['page']}")
                
                # Save assistant message
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })
            except Exception as e:
                st.error(f"Error processing prompt: {e}")

                





                
