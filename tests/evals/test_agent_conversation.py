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
                    judge_error = metric_infra_error(metrics)
                    if judge_error:
                        metric_error = judge_error
                        infra = judge_error
                    else:
                        metric_error = str(exc)
                except Exception as exc:
                    metric_error = f"{type(exc).__name__}: {exc}"
                    infra = metric_error

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
