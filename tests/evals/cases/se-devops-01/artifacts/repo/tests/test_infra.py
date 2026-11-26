import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class InfraContractTests(unittest.TestCase):
    def test_nginx_matches_api_port(self):
        compose = (ROOT / "docker-compose.yml").read_text(encoding="utf-8")
        nginx = (ROOT / "nginx.conf").read_text(encoding="utf-8")
        self.assertIn("8080:8080", compose)
        self.assertIn("server api:8080;", nginx)
        self.assertNotIn("server api:8000;", nginx)

    def test_worker_healthcheck_matches_ready_file(self):
        dockerfile = (ROOT / "Dockerfile.worker").read_text(encoding="utf-8")
        worker = (ROOT / "app" / "worker.py").read_text(encoding="utf-8")
        self.assertIn("/tmp/worker.ready", worker)
        self.assertIn("/tmp/worker.ready", dockerfile)
        self.assertNotIn("/tmp/worker.ok", dockerfile)

    def test_compose_uses_redis_url(self):
        compose = (ROOT / "docker-compose.yml").read_text(encoding="utf-8")
        self.assertIn("REDIS_URL=", compose)
        self.assertNotIn("REDIS_URI=", compose)

    def test_staging_env_has_required_keys(self):
        env_text = (ROOT / "staging.env").read_text(encoding="utf-8")
        keys = {}
        for line in env_text.splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                keys[k.strip()] = v.strip()
        self.assertTrue(keys.get("REDIS_URL"))
        self.assertTrue(keys.get("PAYMENT_SIGNING_KEY"))
        self.assertNotIn("REDIS_URI", keys)

    def test_deploy_workflow_needs_existing_jobs(self):
        wf = (ROOT / ".github" / "workflows" / "deploy.yml").read_text(encoding="utf-8")
        self.assertNotIn("unit-test", wf)
        self.assertRegex(wf, r"needs:\s*\[\s*lint\s*,\s*tests\s*\]")

    def test_smoke_check_passes(self):
        proc = subprocess.run(
            ["bash", "scripts/smoke_check.sh"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stdout + proc.stderr)
        self.assertIn("worker ok", proc.stdout)


if __name__ == "__main__":
    unittest.main()
