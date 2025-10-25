#!/usr/bin/env python3
"""
Simple HTTP server to serve the frontend files
This allows the frontend to make API calls to the backend without CORS issues
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

# Configuration
FRONTEND_PORT = 8081  # Changed from 8080 to avoid port conflicts
FRONTEND_DIR = Path(__file__).parent / "frontend"

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=FRONTEND_DIR, **kwargs)

    def end_headers(self):
        # Add CORS headers to allow API calls to backend
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

def serve_frontend():
    """Start the frontend server"""
    try:
        with socketserver.TCPServer(("", FRONTEND_PORT), CustomHTTPRequestHandler) as httpd:
            print(f"🚀 Frontend server running at: http://localhost:{FRONTEND_PORT}")
            print(f"📂 Serving files from: {FRONTEND_DIR}")
            print(f"🔗 Backend API available at: http://127.0.0.1:8000")
            print("📋 API Documentation at: http://127.0.0.1:8000/docs")
            print("\n💡 Open http://localhost:8080 in your browser to use the app")
            print("🔄 Press Ctrl+C to stop the server")

            # Open browser automatically
            webbrowser.open(f'http://localhost:{FRONTEND_PORT}')

            httpd.serve_forever()

    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped")
    except OSError as e:
        print(f"❌ Error starting server: {e}")
        print(f"💡 Try changing the port or check if port {FRONTEND_PORT} is already in use")

if __name__ == "__main__":
    serve_frontend()