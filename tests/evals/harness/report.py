"""Write per-case artifacts and a run-level benchmark summary."""

from __future__ import annotations

import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

import deepeval

from .case import EVALS_ROOT, Case
from .judge import judge_settings
from ..metrics import metric_scores

RUNS_DIR = EVALS_ROOT / ".runs"


def current_run_id() -> str:
    return os.getenv("EVAL_RUN_ID", "").strip() or datetime.now().strftime("%Y%m%d-%H%M%S")


def case_run_dir(run_id: str, case_id: str) -> Path:
    return RUNS_DIR / run_id / case_id


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, default=str) + "\n",
                    encoding="utf-8")


def _metric_rows(metrics: list[Any] | None) -> list[dict[str, Any]]:
    return metric_scores(metrics or [])


def _metric_failures(rows: list[dict[str, Any]]) -> list[str]:
    return [
        row["name"]
        for row in rows
        if row.get("success") is False or row.get("error")
    ]


def _status(checks, metric_rows: list[dict[str, Any]], metric_error: str | None) -> str:
    if checks.infra_failures:
        return "infra"
    if checks.deterministic_failures or metric_error or _metric_failures(metric_rows):
        return "fail"
    return "pass"


def _final_markdown(case: Case, result, checks, metric_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {case.name} (`{case.id}`)",
        "",
        f"- profile: `{case.profile}`",
        f"- tags: {', '.join(case.tags) or '(none)'}",
        f"- model: `{result.model}` via `{result.provider}`",
        f"- model chain: {' -> '.join(f'`{item}`' for item in (getattr(result, 'model_chain', None) or [])) or '(single)'}",
        f"- fallbacks: {len(getattr(result, 'fallbacks', None) or [])}",
        f"- duration: {result.duration:.1f}s",
        f"- steps: {result.steps}",
        f"- tool calls: {len(result.tool_calls)}",
        f"- truncated: {result.truncated}",
        "",
        "## Input",
        "",
        "```text",
        case.input,
        "```",
        "",
        "## Final output",
        "",
        "```text",
        result.final_output,
        "```",
        "",
    ]
    if case.expected_output:
        lines += ["## Expected output", "", "```text", case.expected_output, "```", ""]

    lines += ["## Checks", "", f"Passed: **{checks.passed}**", ""]
    if checks.failures:
        lines += ["```text", checks.summary(limit=40), "```", ""]

    lines += ["## Metrics", ""]
    if metric_rows:
        lines += ["| Metric | Score | Threshold | Success |", "|---|---|---|---|"]
        for row in metric_rows:
            score = row.get("score")
            score_text = "—" if score is None else f"{float(score):.3f}"
            threshold = row.get("threshold")
            threshold_text = "—" if threshold is None else f"{float(threshold):.3f}"
            lines.append(
                f"| {row.get('name')} | {score_text} | {threshold_text} | {row.get('success')} |"
            )
        lines.append("")
        for row in metric_rows:
            if row.get("reason"):
                lines += [f"**{row.get('name')}**: {row['reason']}", ""]
    else:
        lines += ["(no metrics)", ""]

    lines += ["## Tool calls", ""]
    if result.tool_calls:
        for index, call in enumerate(result.tool_calls, start=1):
            preview = json.dumps(call.args, ensure_ascii=False, default=str)[:300]
            lines.append(f"{index}. `{call.name}` ok={call.ok} args={preview}")
    else:
        lines.append("(none)")
    lines.append("")

    lines += ["## Workspace changes", "", "```text",
              json.dumps(result.diff, indent=2, ensure_ascii=False), "```", ""]

    if getattr(result, "fallbacks", None):
        lines += ["## Serving fallbacks", ""]
        for item in result.fallbacks:
            lines.append(
                f"- `{item.get('from')}` -> `{item.get('to')}` "
                f"({item.get('reason')}): {item.get('detail')}"
            )
        lines.append("")
    return "\n".join(lines)


def _summary_row(case: Case, result, checks, metric_rows: list[dict[str, Any]],
                 metric_error: str | None, run_id: str) -> dict[str, Any]:
    return {
        "case": case.id,
        "name": case.name,
        "profile": case.profile,
        "tags": case.tags,
        "status": _status(checks, metric_rows, metric_error),
        "checks_passed": checks.passed,
        "deterministic_failures": [x.name for x in checks.deterministic_failures],
        "infra_failures": [x.name for x in checks.infra_failures],
        "metric_failures": _metric_failures(metric_rows),
        "metrics": {
            row.get("name"): row.get("score") for row in metric_rows
        },
        "steps": result.steps,
        "duration": round(result.duration, 2),
        "tool_calls": len(result.tool_calls),
        "tool_errors": sum(1 for call in result.tool_calls if not call.ok),
        "truncated": result.truncated,
        "timed_out": result.timed_out,
        "model": result.model,
        "provider": result.provider,
        "model_chain": getattr(result, "model_chain", []),
        "fallbacks": getattr(result, "fallbacks", []),
        "run_id": run_id,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }


def _update_summary(run_id: str, row: dict[str, Any]) -> None:
    run_root = RUNS_DIR / run_id
    path = run_root / "summary.json"
    rows: list[dict[str, Any]] = []
    if path.is_file():
        try:
            rows = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            rows = []
    rows = [existing for existing in rows if existing.get("case") != row["case"]]
    rows.append(row)
    rows.sort(key=lambda item: item.get("case", ""))
    _write_json(path, rows)

    header = (
        f"# Eval run `{run_id}`\n\n"
        f"- deepeval: `{deepeval.__version__}`\n"
        f"- judge chain: `{judge_settings()['chain'][0]}` via fallback chain "
        f"{' -> '.join(judge_settings()['chain'])}\n"
        f"- generated: {datetime.now().isoformat(timespec='seconds')}\n\n"
        "| Case | Status | Checks | Metrics | Steps | Time | Model |\n"
        "|---|---|---|---|---|---|---|\n"
    )
    lines = []
    for item in rows:
        metrics = item.get("metrics") or {}
        metric_text = ", ".join(
            f"{name}={score:.2f}" if isinstance(score, (int, float)) else f"{name}=—"
            for name, score in metrics.items()
        ) or "—"
        lines.append(
            f"| {item.get('case')} | {item.get('status')} | "
            f"{'pass' if item.get('checks_passed') else 'fail'} | {metric_text} | "
            f"{item.get('steps')} | {item.get('duration')}s | {item.get('model')} |"
        )
    (run_root / "summary.md").write_text(header + "\n".join(lines) + "\n", encoding="utf-8")


def write_report(
    case: Case,
    result,
    checks,
    metrics: list[Any] | None = None,
    metric_error: str | None = None,
    run_id: str | None = None,
) -> Path:
    run_id = run_id or current_run_id()
    out = case_run_dir(run_id, case.id)
    out.mkdir(parents=True, exist_ok=True)

    # Manifest snapshot (a copy keeps the report self-contained).
    if case.path.is_file():
        shutil.copy2(case.path, out / "case.toml")

    _write_json(out / "workspace_manifest_before.json", result.before)
    _write_json(out / "workspace_manifest_after.json", result.after)
    _write_json(out / "workspace_diff.json", result.diff)
    _write_json(out / "tool_calls.json", [call.to_dict() for call in result.tool_calls])
    _write_json(out / "checks.json", checks.to_dict())
    _write_json(out / "result.json", result.to_dict())

    metric_rows = _metric_rows(metrics)
    _write_json(out / "metrics.json", metric_rows)
    if metric_error:
        (out / "metric_error.txt").write_text(metric_error, encoding="utf-8")
    elif (out / "metric_error.txt").exists():
        (out / "metric_error.txt").unlink()

    if result.transcript_path and Path(result.transcript_path).is_file():
        shutil.copy2(result.transcript_path, out / "transcript.jsonl")

    (out / "final.md").write_text(
        _final_markdown(case, result, checks, metric_rows), encoding="utf-8"
    )

    row = _summary_row(case, result, checks, metric_rows, metric_error, run_id)
    _update_summary(run_id, row)
    return out
