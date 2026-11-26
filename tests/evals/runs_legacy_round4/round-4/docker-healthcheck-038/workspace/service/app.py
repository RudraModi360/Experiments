#!/usr/bin/env python3
import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

class AppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = self.path.split("?")[0]
        if parsed_path == "/healthz":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode("utf-8"))
        elif parsed_path == "/":
            token = os.environ.get("APP_TOKEN", "")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            # Respond with service info and masked/prefix token status
            response_data = {
                "message": "Python HTTP Service is running",
                "token_configured": bool(token),
                "token_prefix": token[:4] if token else ""
            }
            self.wfile.write(json.dumps(response_data).encode("utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not Found"}).encode("utf-8"))

    def log_message(self, format, *args):
        # Structured or concise logging if needed, or suppress/standardize
        print(f"[{self.log_date_time_string()}] {self.client_address[0]} - {format%args}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    server_address = ("0.0.0.0", port)
    httpd = HTTPServer(server_address, AppHandler)
    print(f"Starting server on port {port}...", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
