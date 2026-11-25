"""Parametrized DeepEval suite: one single-turn test per discovered case.

The verdict comes ONLY from DeepEval LLM metrics. Deterministic workspace
checks (files, verification commands, custom checks) are collected as evidence
and fed to the GEval judges via the Golden ``context``; they inform the judge
but never gate the result on their own. Infrastructure failures (model /
connection / timeout) are reported as infra, not scored as quality.

Run with ``deepeval test run tests/evals/test_agent_eval.py``. A plain
``pytest`` run skips these tests (see ``conftest.py``).
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
from tests.evals.harness.runner import make_golden, run_traced_case
from tests.evals.harness.workspace import create_workspace
from tests.evals.metrics import metric_infra_error, metrics_for

RUN_ID = current_run_id()
os.environ.setdefault("EVAL_RUN_ID", RUN_ID)

CASES = [case for case in discover_cases() if not case.turns]
CASE_NUMBER = {case.id: index for index, case in enumerate(CASES, 1)}


def _infra_detail(result, checks) -> str | None:
    if result.error:
        return result.error
    if checks.infra_failures:
        return "; ".join(f"{r.name}: {r.detail}" for r in checks.infra_failures)
    return None


@pytest.mark.parametrize("case", CASES, ids=[case.id for case in CASES])
def test_agent_case(case):
    with CaseProgress(case, CASE_NUMBER[case.id], len(CASES), suite="single") as progress:
        with create_workspace(case) as workspace:
            result = run_traced_case(case, workspace, progress=progress)
            progress.set_phase("checks")
            checks = evaluate_checks(case, result, workspace)  # evidence, not a gate

            infra = _infra_detail(result, checks)
            metrics = []
            metric_error: str | None = None

            if infra is None:
                metrics = metrics_for(case, result)
                golden = make_golden(case, result, checks)
                progress.set_phase("judging")
                try:
                    assert_test(golden=golden, metrics=metrics)
                except AssertionError as exc:
                    # DeepEval also raises AssertionError when a judge call
                    # failed and no score was produced; that is infra, not a
                    # quality verdict.
                    judge_error = metric_infra_error(metrics)
                    if judge_error:
                        metric_error = judge_error
                        infra = judge_error
                    else:
                        metric_error = str(exc)  # LLM metric threshold failure = the verdict
                except Exception as exc:  # judge/connection failure, not a quality score
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
                raise AssertionError("DeepEval metric verdict failed:\n" + metric_error)


if __name__ == "__main__":
    raise SystemExit(
        "This is a DeepEval eval suite, not a plain Python script.\n\n"
        "Run one case with:\n"
        "  deepeval test run tests/evals/test_agent_eval.py -k <case-id>\n\n"
        "or use the harness CLI:\n"
        "  python3 -m tests.evals.harness.cli run --case <case-id>\n"
    )
