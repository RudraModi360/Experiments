from __future__ import annotations
import subprocess
from tests.evals.harness.checks import CheckResult


def check(ctx):
    repo = ctx.workspace.root / "repo"
    proc = subprocess.run(
        ["python3", "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    return [
        CheckResult(
            "infra_unittest_suite",
            proc.returncode == 0,
            (proc.stdout + proc.stderr)[-400:],
        )
    ]
