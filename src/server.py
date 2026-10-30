import os
import json
import http.server
import socketserver
from urllib.parse import parse_qs, urlparse

PORT = int(os.environ.get("PORT", 8000))
WEB_DIR = os.path.join(os.path.dirname(__file__), "web")

class NexusRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b'{}'
        
        try:
            payload = json.loads(post_data.decode('utf-8'))
        except json.JSONDecodeError:
            payload = {}

        if self.path == '/api/log':
            self.handle_log(payload)
        elif self.path == '/api/payroll':
            self.handle_payroll(payload)
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        if self.path == '/api/status':
            self.handle_status()
        else:
            super().do_GET()

    def handle_log(self, payload):
        category = payload.get('category', 'general')
        content = payload.get('content', '')
        
        # Import and execute logger dynamically
        from logger import log_entry
        log_entry(category, content)

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response = {"status": "success", "message": f"Log entry [{category.upper()}] recorded."}
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def handle_payroll(self, payload):
        try:
            hours = float(payload.get('hours', 0))
            hourly_rate = float(payload.get('rate', 22.50)) # Default counselor rate
            tax_rate = float(payload.get('tax_rate', 0.22)) # Estimated tax/deduction rate

            gross_pay = hours * hourly_rate
            estimated_net = gross_pay * (1.0 - tax_rate)

            # Wealth Distribution Model (% Allocation of Net Pay)
            allocations = {
                "household_bills": round(estimated_net * 0.40, 2), # 40% Household & Bills
                "subaru_and_auto": round(estimated_net * 0.20, 2),  # 20% STI Loan (M&T) & GEICO
                "kids_growth": round(estimated_net * 0.15, 2),       # 15% Split for 2 Kids
                "tristate_home": round(estimated_net * 0.15, 2),     # 15% Tri-State Home Fund
                "trading_reserve": round(estimated_net * 0.10, 2)   # 10% Topstep / Futures Capital
            }

            breakdown = {
                "hours_worked": hours,
                "hourly_rate": hourly_rate,
                "gross_pay": round(gross_pay, 2),
                "estimated_net": round(estimated_net, 2),
                "vault_distribution": allocations
            }

            # Automatically commit breakdown log to GitHub
            from logger import log_entry
            log_entry("PAYROLL_VAULT", json.dumps(breakdown))

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "data": breakdown}).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))

    def handle_status(self):
        from nexus_status import get_status
        output = get_status()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"output": output}).encode('utf-8'))

if __name__ == "__main__":
    print(f"Starting NEXUS Server on port {PORT}...")
    with socketserver.TCPServer(("", PORT), NexusRequestHandler) as httpd:
        httpd.serve_forever()
