"""
GramSetu AI - Local Ollama Client
Manages streaming & non-streaming communication with local Ollama instance.
"""
import urllib.request
import urllib.error
import json
from core.config import OLLAMA_URL, OLLAMA_MODEL

def stream_chat_from_ollama(messages: list, model: str = None):
    """
    Generator yielding response token strings from local Ollama /api/chat.
    """
    target_model = model or OLLAMA_MODEL
    url = f"{OLLAMA_URL}/api/chat"
    
    payload = {
        "model": target_model,
        "messages": messages,
        "stream": True,
        "options": {
            "temperature": 0.15,
            "top_p": 0.80,
            "repeat_penalty": 1.45,
            "num_predict": 320,
            "stop": [
                "<|im_end|>", "<|im_start|>", "\n\n\n",
                "User:", "\nUser:", "Human:", "\nHuman:",
                "Assistant:", "\nAssistant:", "[Confirmed", "[Verified"
            ]
        }
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            for line in resp:
                if line:
                    try:
                        chunk = json.loads(line.decode("utf-8"))
                        token = chunk.get("message", {}).get("content", "")
                        if token:
                            yield token
                    except Exception:
                        pass
    except Exception as e:
        yield f"\n[Ollama local bridge error: {str(e)}. Running with local verified database.]"

def generate_chat_sync(messages: list, model: str = None) -> str:
    tokens = list(stream_chat_from_ollama(messages, model=model))
    return "".join(tokens)
