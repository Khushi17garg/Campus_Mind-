import json
import re
from query import generate_answer

def generate_flashcards(course_name: str, topic_or_page: str = ""):
    """
    Generates clean, JSON-only flashcards from ingested PDFs.
    """
    focus = f"Focus strictly on the topic or concept: '{topic_or_page}'." if topic_or_page else "Extract key core concepts and definitions."

    prompt = f"""
    You are a strict JSON generator. Extract 5 study flashcards from the retrieved course materials.
    {focus}

    CRITICAL RULES:
    1. Do NOT explain what you are doing.
    2. Do NOT say "Since Page X is not mentioned...".
    3. Output ONLY a valid JSON list of objects.

    JSON FORMAT TO FOLLOW EXACTLY:
    [
        {{
            "id": 1,
            "concept": "Concept Name / Question",
            "definition": "Clear concise definition or explanation.",
            "category": "Core Concept"
        }}
    ]
    """
    query_str = f"Generate study flashcards. {focus}"
    raw_response, sources = generate_answer(course_name, query_str)

    # 1. Clean and parse JSON
    try:
        cleaned = re.sub(r"```json|```", "", raw_response).strip()
        match = re.search(r"\[.*\]", cleaned, re.DOTALL)
        if match:
            cards = json.loads(match.group(0))
            # Ensure concept doesn't contain LLM conversational chatter
            valid_cards = []
            for c in cards:
                if isinstance(c, dict) and "concept" in c and "definition" in c:
                    if not c["concept"].startswith("Since") and len(c["concept"]) < 100:
                        valid_cards.append(c)
            if valid_cards:
                return valid_cards, sources
    except Exception as e:
        print(f"Flashcard parsing error: {e}")

    # 2. Smart fallback if JSON parsing missed
    fallback_cards = []
    lines = [line.strip() for line in raw_response.split('\n') if line.strip()]
    for idx, line in enumerate(lines, start=1):
        if ":" in line and not line.lower().startswith("since") and not line.lower().startswith("here"):
            parts = line.split(":", 1)
            fallback_cards.append({
                "id": idx,
                "concept": parts[0].strip("- *1234567890."),
                "definition": parts[1].strip(),
                "category": "Key Concept"
            })
            if len(fallback_cards) >= 5:
                break

    return fallback_cards, sources



