"""Contract tests: the source of truth. Reads settings.json at run time."""
import json
import os
import subprocess
import sys
import time
import unittest
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PORT = 8765


def _settings():
    return json.loads((ROOT / "settings.json").read_text())


class ContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proc = subprocess.Popen(
            [sys.executable, str(ROOT / "server.py")],
            cwd=str(ROOT), env={**os.environ, "PORT": str(PORT)},
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        for _ in range(50):
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{PORT}/healthz", timeout=1)
                break
            except Exception:
                time.sleep(0.1)

    @classmethod
    def tearDownClass(cls):
        cls.proc.terminate()
        try:
            cls.proc.wait(timeout=5)
        except Exception:
            cls.proc.kill()

    def _get(self, path):
        with urllib.request.urlopen(f"http://127.0.0.1:{PORT}{path}", timeout=2) as r:
            return r.status, json.loads(r.read())

    def test_healthz(self):
        status, body = self._get("/healthz")
        self.assertEqual(status, 200)
        self.assertEqual(body["status"], "ok")

    def test_motd_matches_current_settings(self):
        _, body = self._get("/")
        self.assertEqual(body["motd"], _settings()["motd"])

    def test_max_entries_enforced_from_current_settings(self):
        limit = _settings()["max_entries"]
        # The server must cap entries at the CURRENT settings value.
        _, body = self._get("/entries")
        self.assertLessEqual(len(body["entries"]), limit)
        self.assertEqual(body["max_entries"], limit)
