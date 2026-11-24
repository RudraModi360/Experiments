"""Evidence: the fix should be minimal (only the auth module changed)."""
from tests.evals.harness.checks import CheckResult


def check(ctx):
    modified = set(ctx.diff.get("modified", []))
    added = set(ctx.diff.get("added", []))
    # Allow bytecode/cache noise to be ignored; focus on source edits.
    source_modified = {p for p in modified if not p.endswith(".pyc") and "__pycache__" not in p}
    return [
        CheckResult(
            "minimal_diff_only_auth_changed",
            source_modified <= {"repo/app/auth.py"},
            f"modified={sorted(source_modified)} added={sorted(added)}",
        ),
    ]
