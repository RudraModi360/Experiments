#!/usr/bin/env python3
import os, json
from http.server import HTTPServer, BaseHTTPRequestHandler
class H(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path=="/healthz":
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps({"status":"ok"}).encode())
        elif self.path=="/":
            token=os.environ.get("APP_TOKEN","")
            self.send_response(200); self.send_header("Content-Type","text/plain"); self.end_headers()
            self.wfile.write(f"Hello! token prefix: {token[:4]}".encode())
        else:
            self.send_response(404); self.end_headers()
    def log_message(self,*a): pass
if __name__=="__main__":
    port=int(os.environ.get("PORT","8080"))
    HTTPServer(("0.0.0.0",port),H).serve_forever()
