"""
GramSetu AI - SQLite Local Database & Deterministic Storage Engine
"""
import sqlite3
import json
import datetime
from core.config import DB_PATH

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # User Memories Table (Deterministic Identity & Profile Store)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_memories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        memory_type TEXT NOT NULL,
        key TEXT UNIQUE NOT NULL,
        value TEXT NOT NULL,
        confidence REAL DEFAULT 1.0,
        importance INTEGER DEFAULT 3,
        source TEXT DEFAULT 'explicit_user_statement',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );
    """)

    # Conversation History Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        metadata_json TEXT DEFAULT '{}',
        created_at TEXT NOT NULL
    );
    """)

    conn.commit()
    conn.close()

def set_memory(key, value, memory_type="profile", confidence=1.0, importance=3, source="explicit_user_statement"):
    if not key or value is None:
        return
    now = datetime.datetime.utcnow().isoformat()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO user_memories (memory_type, key, value, confidence, importance, source, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(key) DO UPDATE SET
        value = excluded.value,
        memory_type = excluded.memory_type,
        confidence = excluded.confidence,
        importance = excluded.importance,
        source = excluded.source,
        updated_at = excluded.updated_at;
    """, (memory_type, key, str(value).strip(), confidence, importance, source, now, now))
    conn.commit()
    conn.close()

def get_memory(key):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_memories WHERE key = ?", (key,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def get_all_memories():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_memories ORDER BY importance DESC, updated_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def delete_memory(key):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_memories WHERE key = ?", (key,))
    conn.commit()
    conn.close()

def clear_all_memories():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_memories")
    cursor.execute("DELETE FROM conversations")
    conn.commit()
    conn.close()

def save_message(session_id, role, content, metadata=None):
    now = datetime.datetime.utcnow().isoformat()
    meta_str = json.dumps(metadata or {})
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO conversations (session_id, role, content, metadata_json, created_at)
    VALUES (?, ?, ?, ?, ?)
    """, (session_id or "default", role, content, meta_str, now))
    conn.commit()
    conn.close()

def get_recent_messages(session_id="default", limit=10):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT role, content, metadata_json, created_at FROM conversations
    WHERE session_id = ?
    ORDER BY id DESC LIMIT ?
    """, (session_id or "default", limit))
    rows = cursor.fetchall()
    conn.close()
    res = [dict(r) for r in reversed(rows)]
    return res

# Initialize on module load
init_db()
