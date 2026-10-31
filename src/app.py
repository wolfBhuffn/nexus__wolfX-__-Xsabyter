import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

class ReusableHTTPServer(HTTPServer):
    allow_reuse_address = True

class CommandCenterHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Force root requests to load the login page first
        if path == '/' or path == '/index.html':
            path = '/src/web/login.html'
        else:
            path = f'/src/web{path}'
        return os.path.join(os.getcwd(), path.lstrip('/'))

def run(server_class=ReusableHTTPServer, handler_class=CommandCenterHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"[+] Wolf Command Hub active at http://localhost:{port}")
    print(f"[+] Root locked to secure login portal: src/web/login.html")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Shutting down Command Hub...")
        httpd.server_close()

if __name__ == '__main__':
    run()
