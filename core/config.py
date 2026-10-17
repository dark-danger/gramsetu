"""
GramSetu AI - Configuration Module
"""
import os
import sys

# Support PyInstaller bundled executable
if getattr(sys, 'frozen', False):
    BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    # Keep DB in the working folder or user directory so data persists
    APP_DATA_DIR = os.path.dirname(sys.executable)
    DB_PATH = os.path.join(APP_DATA_DIR, "gramsetu.db")
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DB_PATH = os.path.join(BASE_DIR, "gramsetu.db")

PORT = int(os.environ.get("PORT", 8000))
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:3b")

def _resolve_gemini_api_key():
    # 1. Direct environment variable
    env_val = os.environ.get("GEMINI_API_KEY", "").strip()
    if env_val:
        return env_val

    # 2. Check local configuration and key files (gitignored)
    candidates = [
        os.path.join(BASE_DIR, ".env"),
        os.path.join(BASE_DIR, ".gemini_key"),
        os.path.join(os.path.dirname(__file__), "..", ".env"),
        os.path.join(os.path.dirname(__file__), "..", ".gemini_key"),
        os.path.expanduser("~/.gramsetu_gemini.key")
    ]
    for path in candidates:
        if os.path.isfile(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("GEMINI_API_KEY="):
                            return line.split("=", 1)[1].strip().strip('"').strip("'")
                        elif line and not line.startswith("#") and len(line) > 20:
                            return line
            except Exception:
                pass
    return ""

GEMINI_API_KEY = _resolve_gemini_api_key()
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")
MAX_CONTEXT_TURNS = 10

