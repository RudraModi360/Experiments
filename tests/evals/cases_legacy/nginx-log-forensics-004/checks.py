"""Context-stress telemetry (observational evidence for the judge, not a gate).

Records whether the context pipeline fired (clear/spill, compaction) and whether
the agent avoided dumping the whole 2.9MB log in one tool output.
"""
from pathlib import Path

from tests.evals.harness.checks import CheckResult


def _blob(ctx):
    parts = []
    for msg in ctx.history:
        parts.append(str(msg.get("content", "")))
    return "\n".join(parts)


def check(ctx):
    text = _blob(ctx)
    cleared = "[CLEARED" in text
    stale = "[STALE:" in text
    superseded = "[superseded" in text or "[duplicate:" in text

    spill_files = 0
    home = Path(ctx.run.agent_home) if ctx.run.agent_home else None
    if home and home.exists():
        spill_files = sum(1 for p in home.rglob("*") if p.is_file() and "spill" in str(p))

    compacted = False
    tp = ctx.run.transcript_path
    if tp and Path(tp).exists():
        compacted = "SESSION MEMORY" in Path(tp).read_text(encoding="utf-8", errors="replace")
    compacted = compacted or "SESSION MEMORY" in text

    max_out = max((len(c.output or "") for c in ctx.tool_calls), default=0)

    return [
        CheckResult("telemetry_clear_or_spill_fired", True,
                    f"cleared={cleared} spill_files={spill_files}"),
        CheckResult("telemetry_compaction_fired", True,
                    f"compacted={compacted} stale={stale} dedupe={superseded}"),
        CheckResult("output_discipline_no_full_log_dump", max_out < 900_000,
                    f"largest_tool_output_chars={max_out}"),
    ]
