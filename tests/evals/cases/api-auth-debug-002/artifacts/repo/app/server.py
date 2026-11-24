"""Stdlib HTTP server wiring (not exercised by the unit tests)."""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from .auth import issue_token
from .routes import list_tasks
from .store import Store


def make_server(port=8000, db="tasks.json"):
    store = Store(db)

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            token = self.headers.get("Authorization", "").replace("Bearer ", "")
            body, status = list_tasks(store, token)
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(body).encode())

        def log_message(self, *a):
            pass

    return HTTPServer(("127.0.0.1", port), Handler)
