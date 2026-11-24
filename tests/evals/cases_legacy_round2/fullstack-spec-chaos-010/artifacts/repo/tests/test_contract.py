import json, os, subprocess, sys, time, unittest, urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PORT=8765
def _settings(): return json.loads((ROOT/"settings.json").read_text())
class ContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proc=subprocess.Popen([sys.executable,"server.py"],cwd=ROOT,env={**os.environ,"PORT":str(PORT)})
        time.sleep(1)
    @classmethod
    def tearDownClass(cls):
        cls.proc.terminate(); cls.proc.wait()
    def _get(self,path):
        with urllib.request.urlopen(f"http://127.0.0.1:{PORT}{path}") as r:
            return r.status,json.loads(r.read())
    def test_healthz(self):
        s,b=self._get("/healthz"); self.assertEqual(s,200); self.assertEqual(b["status"],"ok")
    def test_motd_matches_current_settings(self):
        s,b=self._get("/"); self.assertEqual(b["motd"],_settings()["motd"])
    def test_max_entries_enforced_from_current_settings(self):
        s,b=self._get("/entries"); self.assertLessEqual(len(b["entries"]),_settings()["max_entries"]); self.assertEqual(b["max_entries"],_settings()["max_entries"])
if __name__ == "__main__":
    unittest.main()
