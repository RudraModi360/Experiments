"""Evidence: compaction telemetry + contradiction resolved by effective date."""
from pathlib import Path

from tests.evals.harness.checks import CheckResult


def check(ctx):
    text = "\n".join(str(m.get("content", "")) for m in ctx.history)
    home = Path(ctx.run.agent_home) if ctx.run.agent_home else None
    spill = sum(1 for p in home.rglob("*") if p.is_file() and "spill" in str(p)) if home and home.exists() else 0
    compacted = "SESSION MEMORY" in text
    tp = ctx.run.transcript_path
    if tp and Path(tp).exists():
        compacted = compacted or "SESSION MEMORY" in Path(tp).read_text(encoding="utf-8", errors="replace")

    answers = Path(ctx.workspace.root) / "answers.md"
    a = answers.read_text(encoding="utf-8") if answers.exists() else ""
    cites_2026 = "billing-policy-2026" in a
    has_30 = "30 days" in a or "30-day" in a
    # The outdated 14-day window must not be presented as the current answer.
    presents_14_current = ("14 days" in a) and ("current" in a.lower()) and ("30 days" not in a)

    return [
        CheckResult("telemetry_compaction_fired", True, f"compacted={compacted} spill_files={spill}"),
        CheckResult("answer_uses_2026_policy", cites_2026 and has_30 and not presents_14_current,
                    f"cites_2026={cites_2026} has_30_days={has_30} presents_14_current={presents_14_current}"),
    ]
