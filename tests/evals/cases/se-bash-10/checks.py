from __future__ import annotations
import subprocess
from tests.evals.harness.checks import CheckResult


def check(ctx):
    proc = subprocess.run(
        ["bash", "tests/test_backup.sh"],
        cwd=ctx.workspace.root,
        capture_output=True,
        text=True,
    )
    return [CheckResult("backup_rotation_test", proc.returncode == 0, (proc.stdout + proc.stderr)[-400:])]
