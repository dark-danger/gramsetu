#!/usr/bin/env python3
"""
GramSetu AI - Production Server & Agent Orchestrator
Features:
- Deterministic SQLite User Memory & Profile Management
- Language, Intent & Tone Routing Pipeline
- Offline Tools & Curated RAG Engine
- Real-time Token Streaming & Safe Processing Metadata
"""

import http.server
import socketserver
import os
import sys
import json
import urllib.request
import urllib.error

# Core imports
from core.config import PORT, BASE_DIR, OLLAMA_URL, OLLAMA_MODEL
from core.database import (
    get_all_memories, set_memory, clear_all_memories, delete_memory,
    save_message, get_recent_messages
)
from core.router import route_and_prepare
from core.validation import validate_and_sanitize
from ai.prompts import build_messages_for_ollama
from ai.ollama_client import stream_chat_from_ollama

class GramSetuServer(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0, post-check=0, pre-check=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.end_headers()

    def do_GET(self):
        # 1. API: List available models from local Ollama
        if self.path.startswith('/api/tags') or self.path.startswith('/api/ollama/tags'):
            self.proxy_ollama_tags()
            return

        # 2. API: Get all user memories from SQLite
        if self.path.startswith('/api/memories'):
            self.handle_get_memories()
            return

        super().do_GET()

    def do_POST(self):
        # 1. API: Agent Chat Pipeline with Streaming & Deterministic Memory
        if self.path.startswith('/api/chat') or self.path.startswith('/api/agent/chat'):
            self.handle_agent_chat()
            return

        # 2. API: Save Memory manually from UI
        if self.path.startswith('/api/memories/save'):
            self.handle_save_memory()
            return

        # 3. API: Clear all memories
        if self.path.startswith('/api/memories/clear'):
            self.handle_clear_memories()
            return

        # 4. Fallback direct Ollama proxy for legacy generate
        if self.path.startswith('/api/generate') or self.path.startswith('/api/ollama/generate'):
            self.proxy_direct_ollama()
            return

        super().do_POST()

    def proxy_ollama_tags(self):
        try:
            req = urllib.request.Request(f"{OLLAMA_URL}/api/tags")
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = resp.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(data)
        except Exception:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            fallback = json.dumps({"models": [{"name": OLLAMA_MODEL}]}).encode('utf-8')
            self.wfile.write(fallback)

    def handle_get_memories(self):
        mems = get_all_memories()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"memories": mems}).encode('utf-8'))

    def handle_save_memory(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else b'{}'
        try:
            data = json.loads(body.decode('utf-8'))
            key = data.get('key')
            val = data.get('value')
            m_type = data.get('memory_type', 'profile')
            if key and val:
                set_memory(key, val, memory_type=m_type, confidence=1.0, importance=4, source="manual_ui")
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "memories": get_all_memories()}).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

    def handle_clear_memories(self):
        clear_all_memories()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "cleared"}).encode('utf-8'))

    def handle_agent_chat(self):
        """
        Master Agent Pipeline:
        Input -> Language/Intent/Tone -> Memory & Tool Execution -> Qwen Inference -> Validation -> Stream.
        """
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else b'{}'
        
        try:
            req_data = json.loads(body.decode('utf-8'))
            
            # Extract prompt from either direct 'prompt' or 'messages' array
            prompt = ""
            if "prompt" in req_data:
                prompt = req_data["prompt"]
            elif "messages" in req_data and req_data["messages"]:
                last_msg = req_data["messages"][-1]
                prompt = last_msg.get("content", "")

            session_id = req_data.get("session_id", "default")
            requested_model = req_data.get("model", OLLAMA_MODEL)

            if not prompt.strip():
                self.send_response(400)
                self.end_headers()
                return

            # Save user message to database
            save_message(session_id, "user", prompt)

            # 1. Deterministic Router & Preprocessing Pipeline
            routing_info = route_and_prepare(prompt, session_id=session_id)

            # Prepare Safe Processing Metadata for Deep Think Panel
            metadata = {
                "intent": routing_info["intent"],
                "input_language": routing_info["input_language"],
                "output_language": routing_info["output_language"],
                "tone": routing_info["tone"],
                "memories_used": routing_info["relevant_memories"],
                "tools_executed": [t["tool_name"] for t in routing_info["tool_results"]],
                "rag_title": routing_info["rag_item"]["title"] if routing_info.get("rag_item") else None,
                "image_payload": routing_info.get("image_payload")
            }

            # Start Streaming Response Chunked / NDJSON
            self.send_response(200)
            self.send_header('Content-Type', 'application/x-ndjson')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Connection', 'close')
            self.end_headers()

            # First Chunk: Emit Safe Processing Metadata
            meta_chunk = json.dumps({"type": "metadata", "data": metadata}) + "\n"
            self.write_stream(meta_chunk)

            final_accumulated_text = ""

            # CASE A: Direct Deterministic Response (Memory / Conversions / Visuals)
            if not routing_info.get("requires_llm") and routing_info.get("direct_response"):
                direct_ans = routing_info["direct_response"]
                final_accumulated_text = direct_ans
                
                # Stream out direct answer smoothly
                chunk_payload = json.dumps({"type": "token", "token": direct_ans}) + "\n"
                self.write_stream(chunk_payload)

            # CASE B: Execute Qwen via Ollama with Compact Structured Context
            else:
                recent_history = get_recent_messages(session_id, limit=6)
                messages = build_messages_for_ollama(routing_info, recent_history)

                for token in stream_chat_from_ollama(messages, model=requested_model):
                    final_accumulated_text += token
                    chunk_payload = json.dumps({"type": "token", "token": token}) + "\n"
                    self.write_stream(chunk_payload)

            # Response Validation & Sanitization
            sanitized = validate_and_sanitize(final_accumulated_text, routing_info)
            save_message(session_id, "assistant", sanitized, metadata=metadata)

            # Final Done Signal
            done_chunk = json.dumps({"type": "done", "final": sanitized}) + "\n"
            self.write_stream(done_chunk)

        except Exception as e:
            try:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"type": "error", "error": str(e)}).encode('utf-8'))
            except Exception:
                pass

    def write_stream(self, data):
        """Helper to write line-delimited streaming data"""
        try:
            if isinstance(data, str):
                data = data.encode('utf-8')
            self.wfile.write(data)
            self.wfile.flush()
        except Exception:
            pass

    def proxy_direct_ollama(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else None
        target_url = f"{OLLAMA_URL}{self.path}"
        try:
            req = urllib.request.Request(
                target_url,
                data=post_data,
                headers={'Content-Type': 'application/json'} if post_data else {},
                method='POST'
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                self.send_response(resp.status)
                self.send_header('Content-Type', resp.headers.get('Content-Type', 'application/json'))
                self.end_headers()
                while True:
                    chunk = resp.read(4096)
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    self.wfile.flush()
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

if __name__ == '__main__':
    import webbrowser
    import threading
    import time

    os.chdir(BASE_DIR)
    socketserver.TCPServer.allow_reuse_address = True

    def open_browser():
        time.sleep(1.2)
        url = f"http://localhost:{PORT}"
        print(f"🌐 Opening GramSetu AI in your browser: {url}")
        webbrowser.open(url)

    # Automatically open browser if frozen (.exe) or --open / AUTO_OPEN is specified
    if getattr(sys, 'frozen', False) or '--open' in sys.argv or os.environ.get("AUTO_OPEN") == "1":
        threading.Thread(target=open_browser, daemon=True).start()

    with socketserver.TCPServer(("", PORT), GramSetuServer) as httpd:
        print(f"============================================================")
        print(f"🌾 GramSetu AI Production Agent running at http://localhost:{PORT}")
        print(f"⚡ Ollama Local Bridge -> {OLLAMA_URL} ({OLLAMA_MODEL})")
        print(f"💾 SQLite Deterministic Memory -> {DB_PATH}")
        print(f"🌱 100% Offline Multilingual Reasoning System Ready")
        print(f"============================================================")
        sys.stdout.flush()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down GramSetu server.")
            httpd.server_close()

