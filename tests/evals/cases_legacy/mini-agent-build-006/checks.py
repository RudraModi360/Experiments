"""Evidence: demo transcript structure and safe calc implementation."""
import json
import re
from pathlib import Path

from tests.evals.harness.checks import CheckResult


def check(ctx):
    root = Path(ctx.workspace.root)
    results = []

    transcript = root / "demo_transcript.jsonl"
    rows, bad = [], 0
    if transcript.exists():
        for line in transcript.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                rows.append(obj)
                if not (isinstance(obj, dict) and "step" in obj and "action" in obj):
                    bad += 1
            except json.JSONDecodeError:
                bad += 1
    results.append(CheckResult(
        "transcript_step_action_structure",
        bool(rows) and bad == 0,
        f"rows={len(rows)} malformed={bad}",
    ))

    src = (root / "mini_agent.py").read_text(encoding="utf-8") if (root / "mini_agent.py").exists() else ""
    # Arbitrary-code eval is unsafe; a safe parser or restricted eval is expected.
    unsafe = bool(re.search(r"\beval\s*\(", src)) and "ast" not in src and "literal_eval" not in src
    results.append(CheckResult("calc_no_unsafe_eval", not unsafe,
                               f"uses_bare_eval={unsafe}"))
    return results
