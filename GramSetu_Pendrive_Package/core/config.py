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
MAX_CONTEXT_TURNS = 10

