"""Parametrized DeepEval suite for multi-turn (conversational) cases.

Each case declares ``[[turns]]``; the runner drives one persistent agent session
through them and builds a ``ConversationalTestCase``. The verdict comes ONLY
from DeepEval conversational LLM metrics (ConversationCompleteness,
TurnRelevancy, ConversationalGEval). Single-turn metrics are never used here.

Run with ``deepeval test run tests/evals/test_agent_conversation.py``.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pytest
from deepeval import assert_test

from tests.evals.harness.case import discover_cases
from tests.evals.harness.checks import evaluate_checks
from tests.evals.harness.progress import CaseProgress
from tests.evals.harness.report import case_run_dir, current_run_id, write_report
from tests.evals.harness.runner import run_traced_conversation
from tests.evals.harness.workspace import create_workspace
from tests.evals.metrics import conversational_metrics_for, metric_infra_error

RUN_ID = current_run_id()
os.environ.setdefault("EVAL_RUN_ID", RUN_ID)

CASES = [case for case in discover_cases() if case.turns]
CASE_NUMBER = {case.id: index for index, case in enumerate(CASES, 1)}


def _sync_conversational_scores(metrics: list) -> None:
    """Copy scores from DeepEval's global test run when assert_test copies metrics."""
    if not metrics or all(getattr(m, "score", None) is not None or getattr(m, "error", None) for m in metrics):
        return
    try:
        from deepeval.test_run import global_test_run_manager
        run = global_test_run_manager.get_test_run()
        conv_cases = getattr(run, "conversational_test_cases", None) or []
        if not conv_cases:
            return
        data_list = getattr(conv_cases[-1], "metrics_data", None) or []
        by_name = {getattr(d, "name", None): d for d in data_list}
        for m in metrics:
            key = getattr(m, "name", None) or getattr(m, "__name__", None) or type(m).__name__
            d = by_name.get(key)
            if d is None:
                for k, v in by_name.items():
                    if k and (k.lower() in key.lower() or key.lower() in k.lower()):
                        d = v
                        break
            if d is not None and getattr(m, "score", None) is None:
                m.score = getattr(d, "score", None)
                m.success = getattr(d, "success", None)
                m.reason = getattr(d, "reason", None)
                m.error = getattr(d, "error", None)
    except Exception:
        pass


@pytest.mark.parametrize("case", CASES, ids=[case.id for case in CASES])
def test_agent_conversation(case):
    with CaseProgress(case, CASE_NUMBER[case.id], len(CASES), suite="conversation") as progress:
        with create_workspace(case) as workspace:
            test_case, result = run_traced_conversation(case, workspace, progress=progress)
            progress.set_phase("checks")
            checks = evaluate_checks(case, result, workspace)  # evidence, not a gate

            infra = result.error or (
                "; ".join(f"{r.name}: {r.detail}" for r in checks.infra_failures)
                if checks.infra_failures else None
            )
            metrics = []
            metric_error: str | None = None

            if infra is None:
                metrics = conversational_metrics_for(case)
                progress.set_phase("judging")
                try:
                    assert_test(test_case=test_case, metrics=metrics)
                except AssertionError as exc:
                    _sync_conversational_scores(metrics)
                    judge_error = metric_infra_error(metrics)
                    if judge_error:
                        metric_error = judge_error
                        infra = judge_error
                    else:
                        metric_error = str(exc)
                except Exception as exc:
                    _sync_conversational_scores(metrics)
                    metric_error = f"{type(exc).__name__}: {exc}"
                    infra = metric_error
                else:
                    _sync_conversational_scores(metrics)

            failed = infra is not None or metric_error is not None
            if failed and case.workspace.keep_on_failure:
                workspace.keep = True
                workspace.keep_dir = case_run_dir(RUN_ID, case.id) / "workspace"

            progress.set_phase("report")
            write_report(case, result, checks, metrics=metrics,
                         metric_error=metric_error or infra, run_id=RUN_ID)
            progress.finish(result=result, error=metric_error or infra)

            if infra is not None:
                raise AssertionError(f"INFRA (not a quality score): {infra}")
            if metric_error is not None:
                raise AssertionError("DeepEval conversational verdict failed:\n" + metric_error)


if __name__ == "__main__":
    raise SystemExit(
        "Run with: deepeval test run tests/evals/test_agent_conversation.py -k <case-id>\n"
    )
