"""
GramSetu AI - Google Gemini 3.8 Flash Cloud Intelligence Client
Provides world-class reasoning, deep domain knowledge, and high-speed streaming
using the Gemini Generative Language API.
"""

import json
import urllib.request
import urllib.error
from core.config import GEMINI_API_KEY, GEMINI_MODEL

def is_gemini_available() -> bool:
    """Checks if a valid Gemini API key is configured."""
    return bool(GEMINI_API_KEY and len(GEMINI_API_KEY.strip()) > 10)

def stream_chat_from_gemini(system_prompt: str, history: list, user_prompt: str, model: str = None, max_tokens: int = 2048):
    """
    Streams response token chunks directly from Google Gemini API (gemini-3.8-flash).
    Yields string tokens in real-time.
    """
    target_model = model or GEMINI_MODEL
    api_key = GEMINI_API_KEY
    if not api_key:
        yield "\n[Gemini bridge error: No GEMINI_API_KEY configured.]"
        return

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{target_model}:streamGenerateContent?key={api_key}&alt=sse"

    # 1. Format Gemini Chat Contents (User & Model alternating turns)
    contents = []
    
    # Process history turns
    last_role = None
    for turn in history:
        raw_role = turn.get("role", "user")
        content_text = turn.get("content", "").strip()
        if not content_text:
            continue
            
        role = "model" if raw_role in ["assistant", "model", "system"] else "user"
        
        # Gemini requires strictly alternating roles (user -> model -> user -> model)
        if contents and contents[-1]["role"] == role:
            # Append to previous turn parts
            contents[-1]["parts"].append({"text": content_text})
        else:
            contents.append({"role": role, "parts": [{"text": content_text}]})

    # Append current user prompt
    if contents and contents[-1]["role"] == "user":
        contents[-1]["parts"].append({"text": user_prompt})
    else:
        contents.append({"role": "user", "parts": [{"text": user_prompt}]})

    # 2. Build Gemini API Payload
    payload = {
        "contents": contents,
        "generationConfig": {
            "temperature": 0.45,
            "maxOutputTokens": max_tokens or 2048,
            "topP": 0.95
        }
    }

    if system_prompt and system_prompt.strip():
        payload["systemInstruction"] = {
            "parts": [{"text": system_prompt.strip()}]
        }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            for line in resp:
                line_str = line.decode("utf-8").strip()
                if not line_str:
                    continue
                if line_str.startswith("data:"):
                    json_str = line_str[5:].strip()
                    if not json_str:
                        continue
                    try:
                        chunk = json.loads(json_str)
                        candidates = chunk.get("candidates", [])
                        if candidates:
                            parts = candidates[0].get("content", {}).get("parts", [])
                            for p in parts:
                                token = p.get("text", "")
                                if token:
                                    yield token
                    except Exception:
                        pass
    except Exception as e:
        yield f"\n[Gemini bridge error: {str(e)}. Seamlessly engaging local verified intelligence.]"

def generate_gemini_sync(system_prompt: str, history: list, user_prompt: str, model: str = None) -> str:
    """Non-streaming synchronous generator."""
    tokens = list(stream_chat_from_gemini(system_prompt, history, user_prompt, model=model))
    return "".join(tokens)
