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
    Streams response token chunks directly from Google Gemini API.
    Supports automatic multi-model fallback across Gemini 3.5 Flash, 3.5 Flash-Lite, and 3.8 Flash.
    """
    api_key = GEMINI_API_KEY
    if not api_key:
        yield "\n[Gemini bridge error: No GEMINI_API_KEY configured.]"
        return

    primary_model = model or GEMINI_MODEL
    candidate_models = [primary_model]
    for alt in ["gemini-3.5-flash", "gemini-3.5-flash-lite", "gemini-3.7-flash", "gemini-3.8-flash"]:
        if alt not in candidate_models:
            candidate_models.append(alt)

    # 1. Format Gemini Chat Contents (User & Model alternating turns)
    contents = []
    for turn in history:
        raw_role = turn.get("role", "user")
        content_text = turn.get("content", "").strip()
        if not content_text:
            continue
        role = "model" if raw_role in ["assistant", "model", "system"] else "user"
        if contents and contents[-1]["role"] == role:
            contents[-1]["parts"].append({"text": content_text})
        else:
            contents.append({"role": role, "parts": [{"text": content_text}]})

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

    last_error = None
    for cur_model in candidate_models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{cur_model}:streamGenerateContent?key={api_key}&alt=sse"
        max_retries = 2
        for attempt in range(max_retries):
            req = urllib.request.Request(
                url,
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            try:
                tokens_yielded = 0
                with urllib.request.urlopen(req, timeout=30) as resp:
                    for line in resp:
                        line_str = line.decode("utf-8").strip()
                        if not line_str or not line_str.startswith("data:"):
                            continue
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
                                        tokens_yielded += 1
                                        yield token
                        except Exception:
                            pass
                if tokens_yielded > 0:
                    return  # Successfully finished streaming from cur_model
            except urllib.error.HTTPError as e:
                last_error = f"HTTP Error {e.code}: {e.reason} on {cur_model}"
                if e.code in [429, 503] and attempt < max_retries - 1:
                    import time
                    time.sleep(1.0)
                    continue
                # If 429 or quota exceeded, break to next candidate model
                break
            except Exception as e:
                last_error = f"{str(e)} on {cur_model}"
                break

    # If all candidate models exhausted
    if last_error:
        yield f"\n[Gemini bridge error: {last_error}. Seamlessly engaging local verified intelligence.]"

def generate_gemini_sync(system_prompt: str, history: list, user_prompt: str, model: str = None) -> str:
    """Non-streaming synchronous generator."""
    tokens = list(stream_chat_from_gemini(system_prompt, history, user_prompt, model=model))
    return "".join(tokens)
