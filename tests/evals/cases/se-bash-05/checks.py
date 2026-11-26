from __future__ import annotations
import subprocess
from tests.evals.harness.checks import CheckResult


def check(ctx):
    proc = subprocess.run(
        ["bash", "tests/verify_shell.sh"],
        cwd=ctx.workspace.root,
        capture_output=True,
        text=True,
    )
    return [CheckResult("verify_shell", proc.returncode == 0, (proc.stdout + proc.stderr)[-400:])]
