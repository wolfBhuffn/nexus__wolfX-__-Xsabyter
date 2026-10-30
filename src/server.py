import os
import json
import http.server
import socketserver

PORT = int(os.environ.get("PORT", 8000))
WEB_DIR = os.path.join(os.path.dirname(__file__), "web")

class NexusRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def do_GET(self):
        if self.path == '/analytics':
            self.path = '/analytics.html'
            return super().do_GET()
        elif self.path == '/api/status':
            self.handle_status()
        elif self.path == '/api/content':
            self.handle_content()
        elif self.path == '/api/tournament/leaderboard':
            self.handle_tournament_leaderboard()
        elif self.path == '/api/tournament/telemetry':
            self.handle_tournament_telemetry()
        else:
            super().do_GET()

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
        elif self.path == '/api/trade':
            self.handle_trade(payload)
        elif self.path == '/api/webhook/trade':
            self.handle_trade_webhook(payload)
        elif self.path == '/api/tournament/signal':
            self.handle_tournament_signal(payload)
        else:
            self.send_response(404)
            self.end_headers()

    def handle_log(self, payload):
        category = payload.get('category', 'general')
        content = payload.get('content', '')
        from logger import log_entry
        log_entry(category, content)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "success", "message": f"Log entry [{category.upper()}] recorded."}).encode('utf-8'))

    def handle_payroll(self, payload):
        try:
            reg_hours = float(payload.get('reg_hours', 0))
            ot_hours = float(payload.get('ot_hours', 0))
            hourly_rate = float(payload.get('rate', 20.00))
            tax_rate = float(payload.get('tax_rate', 0.22))

            ot_rate = hourly_rate * 1.5
            reg_pay = reg_hours * hourly_rate
            ot_pay = ot_hours * ot_rate
            gross_pay = reg_pay + ot_pay
            estimated_net = gross_pay * (1.0 - tax_rate)

            allocations = {
                "household_bills": round(estimated_net * 0.40, 2),
                "subaru_and_auto": round(estimated_net * 0.20, 2),
                "kids_growth": round(estimated_net * 0.15, 2),
                "tristate_home": round(estimated_net * 0.15, 2),
                "trading_reserve": round(estimated_net * 0.10, 2)
            }

            breakdown = {
                "biweekly_cycle": True,
                "regular_hours": reg_hours,
                "ot_hours": ot_hours,
                "base_rate": hourly_rate,
                "ot_rate": ot_rate,
                "gross_pay": round(gross_pay, 2),
                "estimated_net": round(estimated_net, 2),
                "vault_distribution": allocations
            }

            from logger import log_entry
            log_entry("PAYROLL_BIWEEKLY", json.dumps(breakdown))

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "data": breakdown}).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))

    def handle_trade(self, payload):
        try:
            symbol = payload.get('symbol', 'NQ').upper()
            contracts = int(payload.get('contracts', 1))
            pnl = float(payload.get('pnl', 0.0))
            notes = payload.get('notes', '')

            trade_entry = {
                "symbol": symbol,
                "contracts": contracts,
                "pnl": pnl,
                "notes": notes,
                "status": "WIN" if pnl > 0 else ("LOSS" if pnl < 0 else "BE")
            }

            from logger import log_entry
            log_entry("FUTURES_TRADE", json.dumps(trade_entry))

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "data": trade_entry}).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))

    def handle_trade_webhook(self, payload):
        from trading_agent import evaluate_and_execute_signal
        result = evaluate_and_execute_signal(payload)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "processed", "result": result}).encode('utf-8'))

    def handle_tournament_signal(self, payload):
        from tournament_engine import evaluate_tournament_signal
        engine_name = payload.get("engine", "Alpha_TechScanner")
        signal = payload.get("signal", {})
        result = evaluate_tournament_signal(engine_name, signal)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "processed", "result": result}).encode('utf-8'))

    def handle_tournament_leaderboard(self):
        from tournament_engine import get_leaderboard
        board = get_leaderboard()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "success", "leaderboard": board}).encode('utf-8'))

    def handle_tournament_telemetry(self):
        telemetry_stream = [
            {"timestamp": "SESSION_OPEN", "category": "ALPHA_TECHSCANNER", "content": "NQ 15m FVG Sweep detected @ 18250.25 -> Signal Executed [2 NQ]"},
            {"timestamp": "SESSION_OPEN", "category": "BETA_ORDERFLOW", "content": "Tape delta spike on ES -> Validated Orderflow Setup [1 NQ]"},
            {"timestamp": "SESSION_OPEN", "category": "GAMMA_SIGNALPARSER", "content": "Community Webhook Signal Received -> Verified [1 MNQ]"}
        ]
        try:
            from logger import get_logs
            all_logs = get_logs()
            if all_logs:
                for entry in all_logs:
                    telemetry_stream.append(entry)
        except Exception:
            pass

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "success", "stream": telemetry_stream[-10:]}).encode('utf-8'))

    def handle_content(self):
        from content_engine import generate_daily_content
        staged_content = generate_daily_content()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "success", "data": staged_content}).encode('utf-8'))

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
