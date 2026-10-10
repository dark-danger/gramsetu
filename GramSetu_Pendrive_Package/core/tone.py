"""
GramSetu AI - Tone Detection Engine
Detects tone and returns directives that actively influence response generation.
"""
import re

def detect_tone(text: str) -> dict:
    lower = text.lower()

    # 1. Urgent / Emergency
    if re.search(r'\b(urgent|emergency|hospital|snake|saanp|bite|katna|current|shock|aag|fire|blood|khoon|poison|zehar)\b', lower):
        return {
            "tone": "urgent",
            "style_prompt": "URGENT SAFETY TONE: Be direct, concise, and immediately prioritize life-saving steps without preamble."
        }

    # 2. Frustrated / Confused
    if re.search(r'\b(problem|error|galat|nahi ho raha|bekar|kharab|frustrated|gussa|samajh nahi ara|mujha smjh ni|dhang se|kyu nahi)\b', lower):
        return {
            "tone": "frustrated",
            "style_prompt": "EMPATHETIC & REASSURING TONE: The user is experiencing difficulty. Acknowledge directly, be extra patient, clear, and reassuring."
        }

    # 3. Formal / Professional
    if re.search(r'\b(formal|official|proposal|university|application|report|letter|documentation|memorandum|resignation|statement of purpose)\b', lower):
        return {
            "tone": "formal_professional",
            "style_prompt": "FORMAL PROFESSIONAL TONE: Provide a polished, well-structured, to-the-point document without redundant filler."
        }

    # 4. Technical / Code
    if re.search(r'\b(code|function|class|algorithm|python|arduino|c\+\+|javascript|sql|bug|compile|memory|database|api)\b', lower):
        return {
            "tone": "technical",
            "style_prompt": "TECHNICAL & PRECISE TONE: Provide clean code with direct, to-the-point explanations and zero filler."
        }

    # 5. Casual / Friendly / Colloquial
    if re.search(r'\b(bhai|yaar|dost|kya\s+h[a]*l|kaise\s+ho|kese\s+ho|kuch bata|bore|masti|joke|chutkula|hello|hi|hey|namaste|kiddan|sab\s+badhiya)\b', lower):
        return {
            "tone": "casual_friendly",
            "style_prompt": "CASUAL FRIENDLY TONE: Be approachable and helpful, answering directly to the point."
        }

    # 6. Default / Neutral
    return {
        "tone": "neutral",
        "style_prompt": "DIRECT TO-THE-POINT TONE: Provide clear, accurate, and concise answers directly addressing the question."
    }
