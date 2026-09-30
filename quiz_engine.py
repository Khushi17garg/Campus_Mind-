import json
import re
from query import generate_answer

def generate_mcq_quiz(course_name: str, quiz_type: str = "3_topic", topic_or_page: str = ""):
    num_questions = 3 if quiz_type == "3_topic" else 10
    focus = f"Focus on: '{topic_or_page}'." if topic_or_page else "Cover core concepts across the context."

    prompt = f"""
    Create {num_questions} multiple-choice questions from the context.
    Output ONLY valid JSON inside a raw list block:
    [
      {{
        "id": 1,
        "question": "Question?",
        "options": ["A) Op1", "B) Op2", "C) Op3", "D) Op4"],
        "answer": "A) Op1",
        "explanation": "Why correct."
      }}
    ]
    """
    raw_response, sources = generate_answer(course_name, prompt)
    
    try:
        # Strip markdown syntax and extract bracket contents
        cleaned = re.sub(r"```json|```", "", raw_response).strip()
        match = re.search(r"\[.*\]", cleaned, re.DOTALL)
        if match:
            return json.loads(match.group(0)), sources
    except Exception as e:
        print(f"Quiz JSON Parse Error: {e}")
        
    return [], []

