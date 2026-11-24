"""Deterministic evidence: output, files, commands, tools, budgets and custom code.

These observations are cheap and reproducible. They are collected as EVIDENCE
for the DeepEval LLM judges (fed into the GEval ``context``) and for the run
report; they do not gate the verdict on their own. Only infrastructure failures
(model / connection / timeout) are treated specially, because they cannot be
scored as quality. A judge failure never hides the file or command evidence.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .case import EVALS_ROOT, Case
from .workspace import Workspace, WorkspaceError, run_command

REPO_ROOT = EVALS_ROOT.parents[1]
TRUNCATION_MARKERS = (
    "Stopped early:",
    "step limit reached",
    "the same call kept repeating without progress",
    "I stopped because:",
)
INFRA_MARKERS = ("Model error:", "Internal error (")


@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str = ""
    kind: str = "deterministic"  # deterministic | infra

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "passed": bool(self.passed),
            "detail": self.detail,
            "kind": self.kind,
        }


@dataclass
class CheckReport:
    results: list[CheckResult] = field(default_factory=list)
    command_results: list[dict[str, Any]] = field(default_factory=list)

    def add(self, name: str, passed: bool, detail: str = "", kind: str = "deterministic") -> None:
        self.results.append(CheckResult(name, bool(passed), detail, kind))

    def extend(self, results: list[CheckResult]) -> None:
        self.results.extend(results)

    @property
    def failures(self) -> list[CheckResult]:
        return [result for result in self.results if not result.passed]

    @property
    def deterministic_failures(self) -> list[CheckResult]:
        return [result for result in self.failures if result.kind != "infra"]

    @property
    def infra_failures(self) -> list[CheckResult]:
        return [result for result in self.failures if result.kind == "infra"]

    @property
    def passed(self) -> bool:
        return not self.failures

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "results": [result.to_dict() for result in self.results],
            "failures": [result.name for result in self.failures],
            "infra_failures": [result.name for result in self.infra_failures],
            "commands": self.command_results,
        }

    def summary(self, limit: int = 12) -> str:
        if self.passed:
            return f"{len(self.results)} checks passed"
        lines = []
        for result in self.failures[:limit]:
            prefix = "INFRA" if result.kind == "infra" else "FAIL"
            lines.append(f"[{prefix}] {result.name}: {result.detail}")
        if len(self.failures) > limit:
            lines.append(f"... and {len(self.failures) - limit} more failures")
        return "\n".join(lines)


@dataclass
class CheckContext:
    case: Case
    run: Any
    workspace: Workspace
    diff: dict[str, list[str]]
    final_output: str
    tool_calls: list[Any]
    history: list[dict[str, Any]]
    checks: CheckReport


# --------------------------------------------------------------------------- helpers


def _resolve(root: Path, relative: str) -> Path:
    root = root.resolve()
    target = (root / (relative or ".")).resolve()
    if target != root and root not in target.parents:
        raise WorkspaceError(f"path escapes the workspace: {relative!r}")
    return target


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _contains(haystack: str, needle: str) -> bool:
    return needle.lower() in haystack.lower()


def _extract_json(text: str) -> Any:
    text = text.strip()
    fenced = re.search(r"```(?:json)?\s*(.+?)```", text, re.DOTALL | re.IGNORECASE)
    if fenced:
        text = fenced.group(1).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end > start:
        try:
            return json.loads(text[start : end + 1])
        except json.JSONDecodeError:
            pass
    start, end = text.find("["), text.rfind("]")
    if start != -1 and end > start:
        try:
            return json.loads(text[start : end + 1])
        except json.JSONDecodeError:
            pass
    return None


def _check_json_schema(output: str, schema_path: Path) -> tuple[bool, str]:
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return False, f"cannot read schema {schema_path}: {exc}"
    payload = _extract_json(output)
    if payload is None:
        return False, "final output does not contain valid JSON"
    try:
        import jsonschema
    except ImportError:
        return False, "jsonschema is not installed; run `pip install jsonschema`"
    try:
        jsonschema.validate(payload, schema)
    except jsonschema.ValidationError as exc:
        location = "/".join(str(part) for part in exc.absolute_path) or "<root>"
        return False, f"schema mismatch at {location}: {exc.message}"
    return True, "valid JSON matching the schema"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


# --------------------------------------------------------------------------- checks


def _output_checks(case: Case, report: CheckReport, output: str) -> None:
    for needle in case.expect.must_contain:
        report.add(
            f"output_contains:{needle[:60]}",
            _contains(output, needle),
            "found" if _contains(output, needle) else "missing from final output",
        )
    for needle in case.expect.must_not_contain:
        report.add(
            f"output_not_contains:{needle[:60]}",
            not _contains(output, needle),
            "absent" if not _contains(output, needle) else "present in final output",
        )
    if case.expect.regex:
        try:
            matched = re.search(case.expect.regex, output, re.MULTILINE | re.DOTALL) is not None
            detail = "matched" if matched else "pattern did not match"
        except re.error as exc:
            matched, detail = False, f"invalid regex: {exc}"
        report.add("output_regex", matched, detail)
    if case.expect.json_schema:
        schema_path = _resolve(case.dir, case.expect.json_schema)
        ok, detail = _check_json_schema(output, schema_path)
        report.add("output_json_schema", ok, detail)


def _file_checks(case: Case, workspace: Workspace, report: CheckReport) -> None:
    for check in case.expect.files:
        try:
            path = _resolve(workspace.root, check.path)
        except WorkspaceError as exc:
            report.add(f"file:{check.path}", False, str(exc))
            continue

        if check.exists is False:
            report.add(f"file:{check.path}:absent", not path.exists(),
                       "absent" if not path.exists() else "file exists")
            continue

        if not path.exists():
            report.add(f"file:{check.path}:exists", False, "file does not exist")
            continue
        if path.is_dir():
            report.add(f"file:{check.path}:exists", check.exists is not False,
                       "path is a directory")
            continue

        if check.exists is True:
            report.add(f"file:{check.path}:exists", True, "file exists")

        try:
            text = _read_text(path)
        except OSError as exc:
            report.add(f"file:{check.path}:readable", False, str(exc))
            continue

        for needle in check.contains:
            report.add(
                f"file:{check.path}:contains:{needle[:50]}",
                needle in text,
                "found" if needle in text else "missing",
            )
        for needle in check.not_contains:
            report.add(
                f"file:{check.path}:not_contains:{needle[:50]}",
                needle not in text,
                "absent" if needle not in text else "present",
            )
        if check.regex:
            try:
                matched = re.search(check.regex, text, re.MULTILINE | re.DOTALL) is not None
                detail = "matched" if matched else "pattern did not match"
            except re.error as exc:
                matched, detail = False, f"invalid regex: {exc}"
            report.add(f"file:{check.path}:regex", matched, detail)
        if check.sha256:
            actual = _sha256(path)
            report.add(
                f"file:{check.path}:sha256",
                actual.lower() == check.sha256.lower(),
                f"expected {check.sha256}, got {actual}",
            )
        if check.min_bytes is not None or check.max_bytes is not None:
            size = path.stat().st_size
            ok = True
            detail = f"{size} bytes"
            if check.min_bytes is not None and size < check.min_bytes:
                ok, detail = False, f"{size} bytes < min {check.min_bytes}"
            if check.max_bytes is not None and size > check.max_bytes:
                ok, detail = False, f"{size} bytes > max {check.max_bytes}"
            report.add(f"file:{check.path}:size", ok, detail)


def _command_checks(case: Case, workspace: Workspace, report: CheckReport) -> None:
    for index, check in enumerate(case.expect.commands, start=1):
        try:
            cwd = _resolve(workspace.root, check.cwd)
        except WorkspaceError as exc:
            report.add(f"command:{index}:cwd", False, str(exc))
            continue
        if not cwd.is_dir():
            report.add(f"command:{index}:cwd", False, f"not a directory: {cwd}")
            continue
        result = run_command(check.command, cwd, check.timeout)
        report.command_results.append(result)
        combined = (result.get("stdout") or "") + "\n" + (result.get("stderr") or "")
        name = f"command:{check.command[:60]}"
        if result.get("timed_out"):
            report.add(name, False, f"timed out after {check.timeout}s")
            continue
        report.add(
            name,
            result.get("exit_code") == check.exit_code,
            f"exit={result.get('exit_code')} expected={check.exit_code}",
        )
        for needle in check.contains:
            report.add(f"{name}:contains:{needle[:40]}", needle in combined,
                       "found" if needle in combined else "missing")
        for needle in check.not_contains:
            report.add(f"{name}:not_contains:{needle[:40]}", needle not in combined,
                       "absent" if needle not in combined else "present")


def _tool_checks(case: Case, tool_calls: list[Any], report: CheckReport) -> None:
    counts: dict[str, int] = {}
    errors: list[str] = []
    for call in tool_calls:
        name = getattr(call, "name", "")
        counts[name] = counts.get(name, 0) + 1
        if not getattr(call, "ok", True):
            errors.append(name)

    for check in case.expect.tools:
        count = counts.get(check.name, 0)
        if check.min_calls:
            report.add(
                f"tool:{check.name}:min_calls",
                count >= check.min_calls,
                f"{count} calls, expected >= {check.min_calls}",
            )
        if check.max_calls is not None:
            report.add(
                f"tool:{check.name}:max_calls",
                count <= check.max_calls,
                f"{count} calls, expected <= {check.max_calls}",
            )

    if case.expected_tools and not case.expect.tools:
        missing = [name for name in case.expected_tools if counts.get(name, 0) == 0]
        report.add(
            "tool:expected_tools_called",
            not missing,
            f"missing: {missing}" if missing else "all expected tools called",
        )

    for name in case.expect.forbidden_tools + case.workspace.deny_tools:
        report.add(
            f"tool:forbidden:{name}",
            counts.get(name, 0) == 0,
            f"{counts.get(name, 0)} calls",
        )

    if case.expect.max_tool_errors is not None:
        report.add(
            "tool:max_errors",
            len(errors) <= case.expect.max_tool_errors,
            f"{len(errors)} failed calls (allowed {case.expect.max_tool_errors}): {errors[:10]}",
        )


def _budget_checks(case: Case, run: Any, report: CheckReport) -> None:
    max_steps = case.expect.max_steps or case.workspace.max_steps
    if max_steps is not None:
        steps = int(getattr(run, "steps", 0) or 0)
        report.add("budget:max_steps", steps <= max_steps, f"{steps} steps (max {max_steps})")
    if case.expect.max_seconds is not None:
        duration = float(getattr(run, "duration", 0.0) or 0.0)
        report.add(
            "budget:max_seconds",
            duration <= case.expect.max_seconds,
            f"{duration:.1f}s (max {case.expect.max_seconds:.1f}s)",
        )

    output = str(getattr(run, "final_output", "") or "")
    markers = [marker for marker in TRUNCATION_MARKERS if marker in output]
    truncated = bool(getattr(run, "truncated", False)) or bool(markers)
    if not case.expect.truncated_ok:
        report.add(
            "budget:not_truncated",
            not truncated,
            f"truncated ({markers or 'loop/step guard'})" if truncated else "completed",
        )


def _workspace_checks(case: Case, diff: dict[str, list[str]], report: CheckReport) -> None:
    changed = set(diff.get("added", [])) | set(diff.get("modified", [])) | set(diff.get("deleted", []))
    for path in case.expect.files_unchanged:
        report.add(
            f"workspace:unchanged:{path}",
            path not in changed,
            "unchanged" if path not in changed else "changed",
        )


def _infra_checks(run: Any, report: CheckReport) -> None:
    output = str(getattr(run, "final_output", "") or "")
    error = getattr(run, "error", None)
    if error:
        report.add("infra:run_error", False, str(error), kind="infra")
    if not output.strip():
        report.add("infra:non_empty_output", False, "agent returned an empty response", kind="infra")
    for marker in INFRA_MARKERS:
        if marker in output:
            report.add(
                "infra:model_call",
                False,
                output.strip().splitlines()[0][:300],
                kind="infra",
            )
            break
    if not report.infra_failures:
        report.add("infra:ok", True, "no infrastructure failure detected", kind="infra")


def _load_custom_checks(case: Case):
    if not case.checks_module:
        return None
    path = _resolve(case.dir, case.checks_module)
    if not path.is_file():
        return None
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))
    name = f"eval_checks_{re.sub(r'[^0-9a-zA-Z_]', '_', case.id)}"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise WorkspaceError(f"cannot import checks module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return getattr(module, "check", None)


def _custom_checks(case: Case, context: CheckContext, report: CheckReport) -> None:
    try:
        check = _load_custom_checks(case)
    except Exception as exc:
        report.add("custom:import", False, f"{type(exc).__name__}: {exc}")
        return
    if check is None:
        if case.checks_module:
            report.add("custom:missing_check", False, "checks module has no `check(ctx)`")
        return
    try:
        results = check(context)
    except Exception as exc:
        report.add("custom:exception", False, f"{type(exc).__name__}: {exc}")
        return
    if results is None:
        return
    if isinstance(results, (CheckResult, dict, bool)):
        results = [results]
    for item in results:
        if isinstance(item, CheckResult):
            report.results.append(item)
        elif isinstance(item, dict):
            report.add(
                str(item.get("name", "custom")),
                bool(item.get("passed")),
                str(item.get("detail", "")),
                str(item.get("kind", "deterministic")),
            )
        elif isinstance(item, bool):
            report.add("custom", item, "boolean result")
        else:
            report.add("custom:invalid", False, f"unsupported result type: {type(item).__name__}")


# --------------------------------------------------------------------------- entry point


def evaluate_checks(case: Case, run: Any, workspace: Workspace) -> CheckReport:
    report = CheckReport()
    diff = getattr(run, "diff", None) or {"added": [], "modified": [], "deleted": []}
    output = str(getattr(run, "final_output", "") or "")
    tool_calls = list(getattr(run, "tool_calls", []) or [])
    history = list(getattr(run, "history", []) or [])

    _infra_checks(run, report)
    _output_checks(case, report, output)
    _file_checks(case, workspace, report)
    _tool_checks(case, tool_calls, report)
    _budget_checks(case, run, report)
    _workspace_checks(case, diff, report)
    _command_checks(case, workspace, report)

    context = CheckContext(
        case=case,
        run=run,
        workspace=workspace,
        diff=diff,
        final_output=output,
        tool_calls=tool_calls,
        history=history,
        checks=report,
    )
    _custom_checks(case, context, report)
    return report
