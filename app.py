import streamlit as st
import os
import subprocess
from query import generate_answer
from quiz_engine import generate_mcq_quiz
from flashcards import generate_flashcards

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
st.caption("Your 100% Offline, Privacy-First Intelligent Academic Tutor")

# Ensure Data Directories Exist
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

# --- Sidebar Controls ---
with st.sidebar:
    st.header("⚙️ Control Panel")
    
    selected_course = st.selectbox(
        "Select Course Focus", 
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
    if st.button("🗑 Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- Main Navigation Tabs ---
tab_chat, tab_quiz, tab_cards = st.tabs(["💬 AI Chat Tutor", "🎯 Interactive Quiz Engine", "🎴 Smart Flashcards"])

# Initialize Chat State
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==================== TAB 1: CHAT TUTOR ====================
with tab_chat:
    st.write("📍 **Quick Prompts:**")
    prompt_input = None
    col1, col2, col3 = st.columns(3)

    if col1.button("📌 Summarize Unit 1 Notes", use_container_width=True):
        prompt_input = "Summarize the core concepts of Unit 1 in bullet points."
    if col2.button("❓ Generate 3 Practice MCQs", use_container_width=True):
        prompt_input = "Generate 3 multiple-choice practice questions (MCQs) with options and key answers based on the material."
    if col3.button("📝 Explain Important Terms", use_container_width=True):
        prompt_input = "List and define the key academic terms and definitions from the context."

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "sources" in message and message["sources"]:
                with st.expander("📚 View Cited Sources"):
                    for src in message["sources"]:
                        st.info(f"📄 **File:** `{src['file']}` | **Page:** {src['page']}")

    chat_prompt = st.chat_input("Ask anything from your course materials...")
    final_prompt = prompt_input or chat_prompt

    if final_prompt and final_prompt.strip():
        st.session_state.messages.append({"role": "user", "content": final_prompt})
        with st.chat_message("user"):
            st.markdown(final_prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing course material..."):
                try:
                    answer, sources = generate_answer(selected_course, final_prompt)
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
                    st.error(f"Error processing prompt: {e}")
# ==================== TAB 2: QUIZ ENGINE ====================
with tab_quiz:
    st.subheader("🎯 Campus Mind Assessment Center")

    quiz_mode = st.radio(
        "Select Assessment Scope:",
        options=["Topic/Page Specific (3 Questions)", "Full Document Exam (10 Questions)"],
        horizontal=True
    )

    topic_input = ""
    if "Topic/Page Specific" in quiz_mode:
        topic_input = st.text_input("Enter Topic Name or Page Focus (e.g., 'Unit 1' or 'Page 10'):")

    if st.button("🚀 Generate Assessment"):
        q_type = "3_topic" if "Topic/Page Specific" in quiz_mode else "10_full"
        with st.spinner("Synthesizing quiz questions from course vector index..."):
            quiz_data, quiz_sources = generate_mcq_quiz(selected_course, quiz_type=q_type, topic_or_page=topic_input)
            st.session_state["active_quiz"] = quiz_data
            st.session_state["quiz_sources"] = quiz_sources
            st.session_state["user_answers"] = {}

    if "active_quiz" in st.session_state and st.session_state["active_quiz"]:
        quiz = st.session_state["active_quiz"]
        st.info(f"📋 **Total Questions:** {len(quiz)}")
        
        with st.form("interactive_quiz_form"):
            for idx, q in enumerate(quiz, start=1):
                st.markdown(f"**Q{idx}: {q['question']}**")
                st.session_state["user_answers"][q["id"]] = st.radio(
                    "Select Choice:",
                    options=q["options"],
                    key=f"q_radio_{q['id']}"
                )
                st.write("---")
                
            submitted = st.form_submit_button("Submit Answers & Grade")
            
        if submitted:
            score = 0
            total = len(quiz)
            
            st.subheader("📊 Quiz Performance Analysis")
            for q in quiz:
                user_ans = st.session_state["user_answers"].get(q["id"])
                correct_ans = q["answer"]
                
                if user_ans == correct_ans:
                    score += 1
                    st.success(f"✅ **Q{q['id']}: Correct!** Choice: {user_ans}")
                else:
                    st.error(f"❌ **Q{q['id']}: Incorrect.** Your choice: `{user_ans}` | Correct: `{correct_ans}`")
                    st.info(f"💡 **Explanation:** {q['explanation']}")
                    
            pct = (score / total) * 100 if total > 0 else 0
            st.metric(label="Final Score", value=f"{score} / {total}", delta=f"{pct:.1f}% Score")
            
            if st.session_state.get("quiz_sources"):
                with st.expander("📚 View Cited Document Pages Used for Quiz"):
                    for src in st.session_state["quiz_sources"]:
                        st.write(f"📄 **File:** `{src['file']}` | **Page:** {src['page']}")

# ==================== TAB 3: SMART FLASHCARDS ====================
with tab_cards:
    st.subheader("🎴 Smart Study Flashcards (Verifiable Memory Deck)")

    fc_topic = st.text_input("Enter Topic / Page Focus for Flashcards (Optional):", key="fc_input")

    if st.button("⚡ Generate Flashcard Deck"):
        with st.spinner("Extracting high-yield concepts and definitions..."):
            cards, fc_sources = generate_flashcards(selected_course, topic_or_page=fc_topic)
            if cards:
                st.session_state["active_flashcards"] = cards
                st.session_state["fc_sources"] = fc_sources
            else:
                st.error("Could not generate flashcards. Please try clicking the button again or providing a more specific topic.")

    if "active_flashcards" in st.session_state and st.session_state["active_flashcards"]:
        cards = st.session_state["active_flashcards"]
        st.write(f"🎴 **Generated {len(cards)} Flashcards**")
        
        for c in cards:
            with st.expander(f"📌 **{c.get('concept', 'Concept')}** (`{c.get('category', 'General')}`)"):
                st.markdown("**Definition / Answer:**")
                st.info(c.get("definition", "No definition provided."))
                
                if st.session_state.get("fc_sources"):
                    st.caption(f"📚 Verified Source: `{st.session_state['fc_sources'][0]['file']}` (Page {st.session_state['fc_sources'][0]['page']})")
                    