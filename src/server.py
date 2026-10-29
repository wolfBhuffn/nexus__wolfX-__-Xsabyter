import http.server
import socketserver
import json
import subprocess
from pathlib import Path
import os
# Render provides a dynamic PORT environment variable; default to 3000 locally
PORT = int(os.environ.get("PORT", 3000))
WEB_DIR = Path("src/web")

class NexusHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        if path == "/":
            return str(WEB_DIR / "index.html")
        return str(WEB_DIR / path.lstrip("/"))

    def do_GET(self):
        if self.path == "/api/status":
            res = subprocess.run(["python3", "src/nexus_status.py"], capture_output=True, text=True)
            self._send_json({"output": res.stdout})
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/api/log":
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length).decode('utf-8'))
            category = post_data.get("category", "idea")
            content = post_data.get("content", "")

            if content:
                res = subprocess.run(["python3", "src/logger.py", "-c", category, content], capture_output=True, text=True)
                self._send_json({"status": "success", "message": f"Entry logged: [{category.upper()}] {content}"})
            else:
                self._send_json({"status": "error", "message": "Content cannot be empty"}, status=400)

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

if __name__ == "__main__":
    server_address = ("0.0.0.0", PORT)
    with socketserver.TCPServer(server_address, NexusHandler) as httpd:
        print(f"[+] NEXUS Web Command Center live on port {PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[-] Server shutting down.")
