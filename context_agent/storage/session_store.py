"""Session storage: transcript, snapshot, spill files and retention pruning."""

from __future__ import annotations

import json
import os
import shutil
import time
import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from ..config import Config
from ..utilities.files import atomic_write_bytes


class SessionStore:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.root = os.path.join(cfg.home, "sessions")
        os.makedirs(self.root, exist_ok=True)
        self.sid = ""
        self.dir = ""

    @property
    def spill_dir(self) -> str:
        return os.path.join(self.dir, "spill")

    def new_session(self) -> str:
        self.sid = datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:4]
        self.dir = os.path.join(self.root, self.sid)
        os.makedirs(self.spill_dir, exist_ok=True)
        return self.sid

    def open_session(self, sid: str) -> bool:
        path = os.path.join(self.root, sid)
        if not os.path.isfile(os.path.join(path, "state.json")):
            return False
        self.sid, self.dir = sid, path
        os.makedirs(self.spill_dir, exist_ok=True)
        return True

    def latest(self) -> Optional[str]:
        try:
            names = sorted((n for n in os.listdir(self.root)
                            if os.path.isfile(os.path.join(self.root, n, "state.json"))), reverse=True)
        except OSError:
            return None
        return names[0] if names else None

    def _started_at(self, sid: str) -> Optional[datetime]:
        """Parse the ``YYYYMMDD-HHMMSS-xxxx`` prefix into a local datetime."""
        try:
            return datetime.strptime(sid[:15], "%Y%m%d-%H%M%S")
        except ValueError:
            return None

    def list_sessions(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Saved sessions, newest first, with timestamps and a short preview.

        Each item: ``sid``, ``started`` (local datetime), ``saved`` (snapshot
        time if present), ``messages``, ``model``, ``preview``.
        """
        items: List[Dict[str, Any]] = []
        try:
            names = os.listdir(self.root)
        except OSError:
            return items
        for name in names:
            state_path = os.path.join(self.root, name, "state.json")
            if not os.path.isfile(state_path):
                continue
            started = self._started_at(name)
            if started is None:
                try:
                    started = datetime.fromtimestamp(os.path.getmtime(state_path))
                except OSError:
                    continue
            data: Dict[str, Any] = {}
            try:
                with open(state_path, "r", encoding="utf-8") as handle:
                    data = json.load(handle)
            except (OSError, ValueError):
                data = {}
            history = data.get("history") or []
            preview = ""
            for msg in history:
                if (msg or {}).get("role") == "user":
                    text = " ".join(str((msg.get("content") or "")).split())
                    if text:
                        preview = text[:70]
                        break
            items.append({
                "sid": name,
                "started": started,
                "saved": data.get("saved"),
                "messages": len(history),
                "model": data.get("model") or "",
                "preview": preview,
            })
        items.sort(key=lambda item: item["started"], reverse=True)
        return items[:limit] if limit else items

    def append_transcript(self, record: Dict[str, Any]) -> None:
        try:
            with open(os.path.join(self.dir, "transcript.jsonl"), "a", encoding="utf-8") as handle:
                handle.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
        except OSError:
            pass

    def append_context_event(self, record: Dict[str, Any]) -> None:
        """Persist one context-maintenance pass for later analysis."""
        try:
            with open(os.path.join(self.dir, "context_events.jsonl"), "a", encoding="utf-8") as handle:
                handle.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
        except OSError:
            pass

    def read_context_events(self, limit: int = 200) -> List[Dict[str, Any]]:
        """Load the newest context-maintenance records for this session."""
        path = os.path.join(self.dir, "context_events.jsonl")
        try:
            with open(path, "r", encoding="utf-8") as handle:
                lines = handle.readlines()
        except OSError:
            return []
        records: List[Dict[str, Any]] = []
        for line in lines[-limit:]:
            try:
                item = json.loads(line)
            except ValueError:
                continue
            if isinstance(item, dict):
                records.append(item)
        return records

    def save_snapshot(self, data: Dict[str, Any]) -> None:
        try:
            payload = json.dumps(data, ensure_ascii=False, default=str).encode("utf-8")
            atomic_write_bytes(os.path.join(self.dir, "state.json"), payload)
        except OSError:
            pass

    def load_snapshot(self) -> Optional[Dict[str, Any]]:
        try:
            with open(os.path.join(self.dir, "state.json"), "r", encoding="utf-8") as handle:
                return json.load(handle)
        except (OSError, ValueError):
            return None

    def prune(self, days: int) -> None:
        cutoff = time.time() - days * 86400
        try:
            for name in os.listdir(self.root):
                path = os.path.join(self.root, name)
                if path != self.dir and os.path.isdir(path) and os.path.getmtime(path) < cutoff:
                    shutil.rmtree(path, ignore_errors=True)
        except OSError:
            pass
