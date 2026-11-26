from __future__ import annotations
import os
import subprocess
from tests.evals.harness.checks import CheckResult


def check(ctx):
    repo = ctx.workspace.root / "repo"
    env = os.environ.copy()
    env["PATH"] = "/opt/homebrew/bin:/usr/local/bin:" + env.get("PATH", "")
    proc = subprocess.run(
        ["node", "--test", "tests/test_checkout.mjs"],
        cwd=repo,
        capture_output=True,
        text=True,
        env=env,
    )
    return [CheckResult("checkout_tests", proc.returncode == 0, (proc.stdout + proc.stderr)[-400:])]
