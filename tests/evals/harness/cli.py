"""``evalctl``: list, validate, run, scaffold, export and inspect eval cases."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from .case import (
    CASES_DIR,
    EVALS_ROOT,
    Case,
    CaseError,
    discover_cases,
    load_case,
    validate_case,
)
from .report import RUNS_DIR, current_run_id
from .serving import describe_chain
from .judge import describe_judge_chain
from ..metrics import resolve_metric_keys

REPO_ROOT = EVALS_ROOT.parents[1]

TEMPLATES: dict[str, str] = {
    "core": """id = "{id}"
name = "{name}"
description = ""
enabled = true
tags = ["core"]
profile = "core"
difficulty = "easy"

input = \"\"\"
{input}
\"\"\"

expected_output = \"\"\"
Describe the required result here. Correctness compares semantically, not by string equality.
\"\"\"

[workspace]
timeout_seconds = 300

[expect]
must_contain = []

[metrics]
profile = "core"
""",
    "smoke": """id = "{id}"
name = "{name}"
enabled = true
tags = ["smoke"]
profile = "smoke"

input = \"\"\"
{input}
\"\"\"

[workspace]
timeout_seconds = 180

[metrics]
profile = "smoke"
""",
    "tools": """id = "{id}"
name = "{name}"
enabled = true
tags = ["tools"]
profile = "tools"

input = \"\"\"
{input}
\"\"\"

expected_output = \"\"\"
Describe the required result here.
\"\"\"

expected_tools = ["read_file"]

[workspace]
timeout_seconds = 300

[metrics]
profile = "tools"
""",
    "code": """id = "{id}"
name = "{name}"
enabled = true
tags = ["code"]
profile = "code"

input = \"\"\"
{input}
\"\"\"

expected_output = \"\"\"
Describe the required code change and the expected passing tests.
\"\"\"

[workspace]
timeout_seconds = 600
# root = "artifacts/repo"

[[workspace.artifacts]]
kind = "repo"
source = "artifacts/repo"
target = "."

[expect]
truncated_ok = false

[[expect.commands]]
command = "python3 -m pytest -q"
cwd = "."
exit_code = 0
timeout = 120

[metrics]
profile = "code"
""",
    "docs": """id = "{id}"
name = "{name}"
enabled = true
tags = ["docs"]
profile = "docs"
grounding = "tool_outputs"

input = \"\"\"
{input}
\"\"\"

expected_output = \"\"\"
Describe the required answer here.
\"\"\"

[[workspace.artifacts]]
kind = "docs"
source = "artifacts/docs"
target = "docs"
transform = "copy"

[workspace]
timeout_seconds = 300

[metrics]
profile = "docs"
""",
    "format": """id = "{id}"
name = "{name}"
enabled = true
tags = ["format"]
profile = "format"

input = \"\"\"
{input}
\"\"\"

expected_output = \"\"\"
Describe the required result here.
\"\"\"

prompt_instructions = [
  "Answer in the exact format requested by the input.",
]

[workspace]
timeout_seconds = 300

[metrics]
profile = "format"
""",
    "conversation": """id = "{id}"
name = "{name}"
enabled = true
tags = ["conversation"]
profile = "conversation"

expected_outcome = \"\"\"
Describe the outcome the whole conversation should reach.
\"\"\"

[workspace]
timeout_seconds = 600

[[turns]]
role = "user"
content = \"\"\"
{input}
\"\"\"

[[turns]]
role = "user"
content = \"\"\"
Follow-up instruction that builds on the first turn.
\"\"\"

[metrics]
profile = "conversation"
""",
}


def _case_table(cases: list[Case]) -> str:
    header = f"{'case':32} {'profile':10} {'metrics':48} {'enabled':7} artifacts"
    lines = [header, "-" * len(header)]
    for case in cases:
        metrics = ", ".join(resolve_metric_keys(case)) or "(none)"
        artifacts = len(case.workspace.artifacts) + (1 if case.workspace.root else 0)
        lines.append(
            f"{case.id:32} {case.profile:10} {metrics[:48]:48} "
            f"{str(case.enabled):7} {artifacts}"
        )
    return "\n".join(lines)


def cmd_list(args) -> int:
    try:
        cases = discover_cases(include_disabled=args.all, strict=False)
    except CaseError as exc:
        print(exc, file=sys.stderr)
        return 2
    print(_case_table(cases))
    return 0


def cmd_validate(args) -> int:
    try:
        cases = discover_cases(include_disabled=True, strict=False)
    except CaseError as exc:
        print(exc, file=sys.stderr)
        return 2

    if args.cases:
        wanted = set(args.cases)
        missing = wanted - {case.id for case in cases}
        cases = [case for case in cases if case.id in wanted]
    else:
        missing = set()

    errors: list[str] = []
    for case in cases:
        errors.extend(validate_case(case))
    ids = [case.id for case in cases]
    duplicates = sorted({case_id for case_id in ids if ids.count(case_id) > 1})
    errors.extend(f"duplicate case id: {case_id}" for case_id in duplicates)
    errors.extend(f"unknown case: {case_id}" for case_id in sorted(missing))

    print(_case_table(cases))
    print()
    if errors:
        print(f"{len(errors)} problem(s):", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print(f"OK: {len(cases)} case(s) valid")
    return 0


def cmd_new(args) -> int:
    case_id = args.case_id.strip()
    if not case_id or "/" in case_id or case_id.startswith("."):
        print("case id must be a simple directory name", file=sys.stderr)
        return 2
    case_dir = CASES_DIR / case_id
    if case_dir.exists() and not args.force:
        print(f"case already exists: {case_dir}", file=sys.stderr)
        return 2
    template = TEMPLATES.get(args.template)
    if template is None:
        print(f"unknown template {args.template!r}; choose from {sorted(TEMPLATES)}", file=sys.stderr)
        return 2

    case_dir.mkdir(parents=True, exist_ok=True)
    (case_dir / "artifacts").mkdir(exist_ok=True)
    if args.template == "code":
        (case_dir / "artifacts" / "repo").mkdir(parents=True, exist_ok=True)
    elif args.template == "docs":
        (case_dir / "artifacts" / "docs").mkdir(parents=True, exist_ok=True)
    name = args.name or case_id.replace("-", " ").title()
    content = template.format(id=case_id, name=name, input=args.input or "Describe the task here.")
    (case_dir / "case.toml").write_text(content, encoding="utf-8")
    print(f"created {case_dir / 'case.toml'}")
    print("Next: add artifacts under artifacts/, then run `evalctl validate`.")
    return 0


def _python() -> str:
    return sys.executable or "python3"


def _deepeval() -> str:
    # Prefer the deepeval executable from the active environment (uv venv), so
    # the eval subprocess uses the same interpreter as the SUT (uzu). sys.prefix
    # stays on the venv even when its python is a symlink to the base interpreter.
    candidate = Path(sys.prefix) / "bin" / "deepeval"
    if candidate.exists():
        return str(candidate)
    sibling = Path(sys.executable).resolve().parent / "deepeval"
    if sibling.exists():
        return str(sibling)
    return shutil.which("deepeval") or "deepeval"


def cmd_run(args) -> int:
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(
        [str(REPO_ROOT), env.get("PYTHONPATH", "")]
    ).strip(os.pathsep)
    # The SUT stays on the local uzu adapter by default; the Gemini key is for
    # the judge. Opt in to a served SUT with EVAL_SERVING_DISABLE=0.
    env.setdefault("EVAL_SERVING_DISABLE", "1")
    env["EVAL_RUN_ID"] = args.run_id or current_run_id()

    if args.cases:
        env["EVAL_CASES"] = ",".join(args.cases)
    if args.include_disabled:
        env["EVAL_INCLUDE_DISABLED"] = "1"
    if args.profile:
        env["EVAL_PROFILE"] = args.profile
    if args.tag:
        env["EVAL_TAG"] = args.tag
    if args.judge_model:
        env["EVAL_JUDGE_MODEL"] = args.judge_model
    if args.judge_provider:
        env["EVAL_JUDGE_PROVIDER"] = args.judge_provider
    if args.judge_base_url:
        env["EVAL_JUDGE_BASE_URL"] = args.judge_base_url
    if args.agent_model:
        env["AGENT_MODEL"] = args.agent_model
    if args.agent_provider:
        env["AGENT_PROVIDER"] = args.agent_provider
    if args.agent_base_url:
        env["AGENT_BASE_URL"] = args.agent_base_url
    if args.serving_chain:
        env["EVAL_SERVING_CHAIN"] = args.serving_chain
    if args.no_serving_fallback:
        env["EVAL_SERVING_DISABLE"] = "1"

    # Keep the CLI honest about which model will actually answer first.
    previous_env = os.environ.copy()
    os.environ.update(env)
    try:
        chain = describe_chain()
    finally:
        os.environ.clear()
        os.environ.update(previous_env)
    if chain:
        print(f"[eval-serving] chain: {chain}")
    else:
        print("[eval-serving] SUT: app default (uzu/qwen unless AGENT_PROVIDER overrides)")
    print(f"[eval-judge] chain: {describe_judge_chain()}")

    suite = getattr(args, "suite", "both")
    files = {
        "single": [EVALS_ROOT / "test_agent_eval.py"],
        "conversation": [EVALS_ROOT / "test_agent_conversation.py"],
        "both": [EVALS_ROOT / "test_agent_eval.py", EVALS_ROOT / "test_agent_conversation.py"],
    }[suite]
    command = [
        _deepeval(), "test", "run",
        *[str(f) for f in files],
        "--identifier", args.identifier or env["EVAL_RUN_ID"],
    ]
    if args.ignore_errors:
        command.append("--ignore-errors")
    if args.skip_on_missing_params:
        command.append("--skip-on-missing-params")
    if args.pytest_args:
        command.extend(["--", *args.pytest_args])

    print("$ " + " ".join(command))
    print(f"run id: {env['EVAL_RUN_ID']}")
    completed = subprocess.run(command, cwd=str(REPO_ROOT), env=env)
    print(f"\nreport: {RUNS_DIR / env['EVAL_RUN_ID'] / 'summary.md'}")
    return completed.returncode


def cmd_export(args) -> int:
    try:
        cases = discover_cases()
    except CaseError as exc:
        print(exc, file=sys.stderr)
        return 2
    rows = []
    for case in cases:
        rows.append(
            {
                "id": case.id,
                "input": case.input,
                "expected_output": case.expected_output or None,
                "expected_tools": [{"name": name} for name in case.expected_tools],
                "context": case.context or None,
                "retrieval_context": case.retrieval_context or None,
                "additional_metadata": {
                    "tags": case.tags,
                    "profile": case.profile,
                    "difficulty": case.difficulty,
                    "description": case.description,
                    **case.metadata,
                },
            }
        )
    output = Path(args.output) if args.output else EVALS_ROOT / ".dataset.json"
    output.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {len(rows)} case(s) to {output}")
    return 0


def cmd_report(args) -> int:
    run_id = args.run_id
    if not run_id:
        runs = sorted((p.name for p in RUNS_DIR.glob("*") if p.is_dir()), reverse=True)
        if not runs:
            print("no runs yet", file=sys.stderr)
            return 1
        run_id = runs[0]
    run_root = RUNS_DIR / run_id
    if not run_root.is_dir():
        print(f"no such run: {run_id}", file=sys.stderr)
        return 1
    if args.case:
        path = run_root / args.case / ("final.md" if not args.json else "result.json")
        if not path.is_file():
            print(f"no report for case {args.case}", file=sys.stderr)
            return 1
        print(path.read_text(encoding="utf-8"))
        return 0
    path = run_root / ("summary.json" if args.json else "summary.md")
    if not path.is_file():
        print(f"missing {path}", file=sys.stderr)
        return 1
    print(path.read_text(encoding="utf-8"))
    return 0


def cmd_import(args) -> int:
    dataset = Path(args.dataset)
    try:
        rows = json.loads(dataset.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"cannot read dataset: {exc}", file=sys.stderr)
        return 2
    if not isinstance(rows, list):
        print("dataset must be a JSON array", file=sys.stderr)
        return 2
    created = 0
    for index, row in enumerate(rows, start=1):
        case_id = str(row.get("id") or f"{args.prefix}-{index:04d}")
        case_dir = CASES_DIR / case_id
        if case_dir.exists():
            continue
        case_dir.mkdir(parents=True)
        tags = ["generated"]
        if args.tag:
            tags.append(args.tag)
        expected_tools = row.get("expected_tools") or []
        if expected_tools and isinstance(expected_tools[0], dict):
            expected_tools = [item.get("name") for item in expected_tools if item.get("name")]
        lines = [
            f'id = "{case_id}"',
            f'name = "{str(row.get("name") or case_id)}"',
            'enabled = false',
            f"tags = {json.dumps(tags)}",
            f'profile = "{args.profile}"',
            "",
            'input = """',
            str(row.get("input") or "").strip(),
            '"""',
            "",
        ]
        if row.get("expected_output"):
            lines += ['expected_output = """', str(row["expected_output"]).strip(), '"""', ""]
        if expected_tools:
            lines.append(f"expected_tools = {json.dumps(expected_tools)}")
            lines.append("")
        if row.get("context"):
            lines.append(f"context = {json.dumps(row['context'])}")
            lines.append("")
        retrieval = row.get("retrieval_context") or (
            row.get("context") if args.profile in {"docs", "full"} else None
        )
        if retrieval:
            lines.append(f"retrieval_context = {json.dumps(retrieval)}")
            lines.append("")
        if args.bundle and args.profile in {"docs", "full"}:
            lines.append('grounding = "tool_outputs"')
            lines.append("")
        lines += ["[workspace]", 'timeout_seconds = 300', ""]
        if args.bundle:
            lines += [
                "[[workspace.artifacts]]",
                'kind = "docs"',
                f'bundle = "{args.bundle}"',
                'target = "docs"',
                'transform = "copy"',
                "",
            ]
        lines += ["[metrics]", f'profile = "{args.profile}"', ""]
        (case_dir / "case.toml").write_text("\n".join(lines), encoding="utf-8")
        created += 1
    print(f"imported {created} case(s) into {CASES_DIR} (disabled until reviewed)")
    return 0


def _rm_path(path: Path) -> bool:
    if not path.exists():
        return False
    if path.is_dir():
        shutil.rmtree(path, ignore_errors=True)
    else:
        try:
            path.unlink()
        except OSError:
            return False
    return True


def cmd_clean(args) -> int:
    """Remove eval run artifacts, traces, caches, and pycache.

    This never touches case sources or case artifacts under tests/evals/cases/.
    Agent sandboxes are created in temp dirs and removed after runs; only
    preserved failure workspaces inside .runs/ are removed here.
    """
    removed: list[str] = []

    if args.run_id:
        target = RUNS_DIR / args.run_id
        if _rm_path(target):
            removed.append(str(target))
        else:
            print(f"no such run: {args.run_id}")
            return 1
    else:
        for p in [RUNS_DIR, EVALS_ROOT / ".cache", EVALS_ROOT / ".generated"]:
            if _rm_path(p):
                removed.append(str(p))
        for p in [EVALS_ROOT / ".dataset.json"]:
            if _rm_path(p):
                removed.append(str(p))
        # DeepEval traces/cache and pytest cache can land at repo root or eval root.
        for p in [REPO_ROOT / ".deepeval", EVALS_ROOT / ".deepeval",
                  REPO_ROOT / ".pytest_cache", EVALS_ROOT / ".pytest_cache"]:
            if _rm_path(p):
                removed.append(str(p))
        if not args.keep_pycache:
            for p in REPO_ROOT.rglob("__pycache__"):
                # Only clean test/eval pycache by default to avoid surprising wipes.
                if "tests" in p.parts and _rm_path(p):
                    removed.append(str(p))

    if removed:
        print("removed:")
        for item in sorted(set(removed)):
            print(f"  - {item}")
    else:
        print("nothing to clean")
    print("\nCase definitions and fixtures were not touched.")
    print("To rerun from scratch: uv run python -m tests.evals.harness.cli run --case <id> --run-id <name>")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="evalctl", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("list", help="list discovered cases")
    p.add_argument("--all", action="store_true", help="include disabled cases")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("validate", help="validate manifests and metric requirements")
    p.add_argument("cases", nargs="*")
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("new", help="scaffold a new case directory")
    p.add_argument("case_id")
    p.add_argument("--template", default="core", choices=sorted(TEMPLATES))
    p.add_argument("--name")
    p.add_argument("--input")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_new)

    p = sub.add_parser("run", help="run cases through deepeval test run")
    p.add_argument("--case", dest="cases", action="append", help="case id (repeatable)")
    p.add_argument("--include-disabled", action="store_true",
                   help="also consider cases with enabled = false")
    p.add_argument("--profile")
    p.add_argument("--tag")
    p.add_argument("--identifier")
    p.add_argument("--run-id")
    p.add_argument("--judge-model")
    p.add_argument("--judge-provider")
    p.add_argument("--judge-base-url")
    p.add_argument("--agent-model")
    p.add_argument("--agent-provider")
    p.add_argument("--agent-base-url")
    p.add_argument("--serving-chain",
                   help="comma-separated provider:model chain, e.g. "
                        "google:gemma-4-31b-it,google:gemini-3.5-flash-lite,ollama:my-model")
    p.add_argument("--no-serving-fallback", action="store_true",
                   help="disable the Google/Ollama serving chain and use AGENT_PROVIDER")
    p.add_argument("--suite", choices=["single", "conversation", "both"], default="both",
                   help="which eval suite to run (default: both)")
    p.add_argument("--ignore-errors", action="store_true", default=True)
    p.add_argument("--skip-on-missing-params", action="store_true", default=True)
    p.add_argument("pytest_args", nargs="*", help="extra pytest args after --")
    p.set_defaults(func=cmd_run)

    p = sub.add_parser("export", help="export enabled cases to .dataset.json")
    p.add_argument("--output")
    p.set_defaults(func=cmd_export)

    p = sub.add_parser("report", help="print the latest or a specific run summary")
    p.add_argument("--run-id")
    p.add_argument("--case")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_report)

    p = sub.add_parser("import", help="import a DeepEval dataset as disabled cases")
    p.add_argument("--dataset", required=True)
    p.add_argument("--bundle")
    p.add_argument("--profile", default="core")
    p.add_argument("--tag")
    p.add_argument("--prefix", default="generated")
    p.set_defaults(func=cmd_import)

    p = sub.add_parser("clean", help="remove run reports, traces, caches (keeps case fixtures)")
    p.add_argument("--run-id", help="remove only this run directory under .runs/")
    p.add_argument("--keep-pycache", action="store_true", help="keep __pycache__ dirs")
    p.set_defaults(func=cmd_clean)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
