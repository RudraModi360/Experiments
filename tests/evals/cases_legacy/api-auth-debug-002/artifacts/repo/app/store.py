"""Tiny JSON-backed task store."""
import json
from pathlib import Path


class Store:
    def __init__(self, path):
        self.path = Path(path)
        self.tasks = []
        if self.path.exists():
            self.tasks = json.loads(self.path.read_text())

    def add(self, title):
        task = {"id": len(self.tasks) + 1, "title": title, "done": False}
        self.tasks.append(task)
        return task

    def all(self):
        return list(self.tasks)
