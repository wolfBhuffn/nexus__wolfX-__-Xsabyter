import os
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler

class CommandCenterHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/ai':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            user_prompt = request_data.get('prompt', '')

            # AI processing logic (integrate your LLM client or response logic here)
            ai_response = f"AI Node Processed: Received query -> '{user_prompt}'"

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response_payload = json.dumps({"status": "success", "reply": ai_response})
            self.wfile.write(response_payload.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def translate_path(self, path):
        if path == '/' or path == '/index.html':
            path = '/src/web/login.html'
        else:
            path = f'/src/web{path}'
        return os.path.join(os.getcwd(), path.lstrip('/'))

def run(server_class=HTTPServer, handler_class=CommandCenterHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"[+] AI-powered Command Hub active at http://localhost:{port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
