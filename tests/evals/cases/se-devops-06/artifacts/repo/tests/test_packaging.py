import re
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PackagingHardeningTests(unittest.TestCase):
    def test_dockerfile_hardened(self):
        df = (ROOT / "Dockerfile").read_text(encoding="utf-8")
        self.assertIn("python:3.12.7-slim", df)
        self.assertNotIn("python:latest", df)
        self.assertGreaterEqual(len(re.findall(r"(?m)^FROM\s+", df)), 2, "Must be multi-stage")
        self.assertRegex(df, r"(?m)^USER\s+(?!root\b)\S+")
        self.assertRegex(df, r"(?m)^HEALTHCHECK\s+")

    def test_requirements_pinned(self):
        lines = [
            l.strip() for l in (ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines()
            if l.strip() and not l.strip().startswith("#")
        ]
        self.assertGreaterEqual(len(lines), 2)
        for line in lines:
            self.assertIn("==", line, f"Unpinned requirement: {line}")

    def test_crontab_fixed(self):
        ct = (ROOT / "cron" / "crontab").read_text(encoding="utf-8")
        self.assertNotIn("/wrong/path/cleanup.sh", ct)
        self.assertIn("scripts/cleanup.sh", ct)

    def test_cleanup_script_spaces_and_errors(self):
        script = ROOT / "scripts" / "cleanup.sh"
        text = script.read_text(encoding="utf-8")
        self.assertIn("set -euo pipefail", text)
        with tempfile.TemporaryDirectory() as td:
            sub = Path(td) / "folder with spaces"
            sub.mkdir()
            tmpf = sub / "old file.tmp"
            keepf = sub / "keep file.txt"
            tmpf.write_text("x", encoding="utf-8")
            keepf.write_text("y", encoding="utf-8")
            proc = subprocess.run(["bash", str(script), str(sub)], capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, msg=proc.stdout + proc.stderr)
            self.assertFalse(tmpf.exists(), "tmp file with spaces was not deleted")
            self.assertTrue(keepf.exists(), "non-tmp file was deleted")

        bad = subprocess.run(["bash", str(script), "/nonexistent_dir_xyz_999"], capture_output=True, text=True)
        self.assertNotEqual(bad.returncode, 0, "cleanup.sh swallowed missing-directory error")


if __name__ == "__main__":
    unittest.main()
