#!/usr/bin/env python3
"""
GramSetu AI - Backend & Local Inference Proxy Server
Serves static assets and provides a transparent, zero-CORS proxy to local Ollama.
"""

import http.server
import socketserver
import os
import sys
import urllib.request
import urllib.error
import json

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
OLLAMA_URL = "http://localhost:11434"

class GramSetuHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

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
        if self.path.startswith('/api/ollama/tags') or self.path == '/api/tags':
            self.proxy_to_ollama('GET', '/api/tags', None)
            return
        super().do_GET()

    def do_POST(self):
        if self.path.startswith('/api/ollama/generate') or self.path == '/api/generate':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length) if content_length > 0 else None
            self.proxy_to_ollama('POST', '/api/generate', post_data)
            return
        elif self.path.startswith('/api/ollama/chat') or self.path == '/api/chat':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length) if content_length > 0 else None
            self.proxy_to_ollama('POST', '/api/chat', post_data)
            return
        super().do_POST()

    def proxy_to_ollama(self, method, endpoint, data):
        target_url = f"{OLLAMA_URL}{endpoint}"
        try:
            req = urllib.request.Request(
                target_url,
                data=data,
                headers={'Content-Type': 'application/json'} if data else {},
                method=method
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
        except urllib.error.URLError as e:
            self.send_response(503)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            err_body = json.dumps({
                "error": "Ollama is not reachable on localhost:11434",
                "detail": str(e),
                "fallback": "Please use GramSetu built-in Offline RAG Engine"
            }).encode('utf-8')
            self.wfile.write(err_body)
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

if __name__ == '__main__':
    os.chdir(DIRECTORY)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), GramSetuHTTPRequestHandler) as httpd:
        print(f"============================================================")
        print(f"🌾 GramSetu AI Production Server running at http://localhost:{PORT}")
        print(f"⚡ Ollama Proxy enabled -> http://localhost:11434")
        print(f"🌱 100% Offline Multi-Modal Rural GenAI System Ready")
        print(f"============================================================")
        sys.stdout.flush()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down GramSetu server.")
            httpd.server_close()
