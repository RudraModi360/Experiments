"""Shared pytest configuration for the eval suite.

The evals only run under ``deepeval test run`` (which sets ``DEEPEVAL=1``), so a
plain ``pytest`` run stays fast and never calls a model by accident.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Fixture repos under cases/*/artifacts contain test files that are intentionally
# broken (they are the tasks). Never collect them as eval tests.
collect_ignore = [str(p) for p in (Path(__file__).parent / "cases").glob("*/artifacts")]

# Keep local runs offline: no Confident AI upload, no telemetry.
os.environ.setdefault("DEEPEVAL_TELEMETRY_OPT_OUT", "1")
os.environ.setdefault("CONFIDENT_API_KEY", "")

# The system under test is the local uzu Qwen model. The Gemini key is for the
# JUDGE, so disable the SUT's Google serving chain by default; opt in with
# EVAL_SERVING_DISABLE=0 and EVAL_SERVING_CHAIN if you want to test a served SUT.
os.environ.setdefault("EVAL_SERVING_DISABLE", "1")


def pytest_collection_modifyitems(config, items):
    if os.environ.get("DEEPEVAL") == "1":
        return
    skip = pytest.mark.skip(
        reason="eval cases run under `deepeval test run` (DEEPEVAL=1), not plain pytest"
    )
    for item in items:
        item.add_marker(skip)
