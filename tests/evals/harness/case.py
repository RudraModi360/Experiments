"""Case registry: load, validate and discover eval cases from ``cases/*/case.toml``."""

from __future__ import annotations

import os
import tomllib
import warnings
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

EVALS_ROOT = Path(__file__).resolve().parents[1]
CASES_DIR = EVALS_ROOT / "cases"
ARTIFACTS_DIR = EVALS_ROOT / "artifacts"

KNOWN_PROFILES = {
    "none", "smoke", "core", "tools", "code", "docs", "format", "safety", "full",
    "conversation",
}
KNOWN_METRICS = {
    "task_completion", "step_efficiency", "correctness", "answer_relevancy",
    "tool_correctness", "argument_correctness", "faithfulness",
    "contextual_relevancy", "code_change_quality", "prompt_alignment",
    "instruction_hierarchy", "cross_file_consistency",
    "bias", "toxicity", "pii_leakage", "plan_adherence", "plan_quality",
    "conversation_completeness", "turn_relevancy", "conversational_correctness",
}
CONVERSATIONAL_METRICS = {
    "conversation_completeness", "turn_relevancy", "conversational_correctness",
}
SINGLE_TURN_METRICS = KNOWN_METRICS - CONVERSATIONAL_METRICS
KNOWN_TRANSFORMS = {
    "copy", "text", "html_to_text", "pdf_to_text", "csv_to_markdown", "unpack",
}
KNOWN_ARTIFACT_KINDS = {"repo", "docs", "file", "inline", "url"}
KNOWN_GROUNDING = {"tool_outputs", "static", "none"}
TOOL_NAMES = {
    "read_file", "write_file", "edit_file", "search_text", "search_files",
    "list_files", "bash", "web_search", "fetch_url", "update_plan", "save_note",
}


class CaseError(Exception):
    """Raised when one or more cases are invalid."""


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


def _as_str(value: Any, default: str = "") -> str:
    return default if value is None else str(value)


def _as_bool(value: Any, default: bool = False) -> bool:
    return default if value is None else bool(value)


def _as_int(value: Any, default: int | None = None) -> int | None:
    return default if value is None else int(value)


def _as_float(value: Any, default: float | None = None) -> float | None:
    return default if value is None else float(value)


@dataclass
class ArtifactSpec:
    kind: str = "file"
    source: str | None = None
    bundle: str | None = None
    target: str = "."
    mode: str = "copy"
    transform: str = "copy"
    include: list[str] = field(default_factory=list)
    exclude: list[str] = field(default_factory=list)
    content: str | None = None
    optional: bool = False
    network: bool = False

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "ArtifactSpec":
        return cls(
            kind=_as_str(raw.get("kind"), "file"),
            source=raw.get("source"),
            bundle=raw.get("bundle"),
            target=_as_str(raw.get("target"), "."),
            mode=_as_str(raw.get("mode"), "copy"),
            transform=_as_str(raw.get("transform"), "copy"),
            include=[str(x) for x in _as_list(raw.get("include"))],
            exclude=[str(x) for x in _as_list(raw.get("exclude"))],
            content=raw.get("content"),
            optional=_as_bool(raw.get("optional"), False),
            network=_as_bool(raw.get("network"), False),
        )


@dataclass
class SetupCommand:
    command: str = ""
    cwd: str = "."
    timeout: int = 60
    optional: bool = False

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "SetupCommand":
        return cls(
            command=_as_str(raw.get("command")),
            cwd=_as_str(raw.get("cwd"), "."),
            timeout=int(raw.get("timeout", 60)),
            optional=_as_bool(raw.get("optional"), False),
        )


@dataclass
class FileCheck:
    path: str = ""
    exists: bool | None = None
    contains: list[str] = field(default_factory=list)
    not_contains: list[str] = field(default_factory=list)
    regex: str | None = None
    sha256: str | None = None
    min_bytes: int | None = None
    max_bytes: int | None = None

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "FileCheck":
        exists = raw.get("exists")
        return cls(
            path=_as_str(raw.get("path")),
            exists=None if exists is None else bool(exists),
            contains=[str(x) for x in _as_list(raw.get("contains"))],
            not_contains=[str(x) for x in _as_list(raw.get("not_contains"))],
            regex=raw.get("regex"),
            sha256=raw.get("sha256"),
            min_bytes=_as_int(raw.get("min_bytes")),
            max_bytes=_as_int(raw.get("max_bytes")),
        )


@dataclass
class CommandCheck:
    command: str = ""
    cwd: str = "."
    exit_code: int = 0
    contains: list[str] = field(default_factory=list)
    not_contains: list[str] = field(default_factory=list)
    timeout: int = 120

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "CommandCheck":
        return cls(
            command=_as_str(raw.get("command")),
            cwd=_as_str(raw.get("cwd"), "."),
            exit_code=int(raw.get("exit_code", 0)),
            contains=[str(x) for x in _as_list(raw.get("contains"))],
            not_contains=[str(x) for x in _as_list(raw.get("not_contains"))],
            timeout=int(raw.get("timeout", 120)),
        )


@dataclass
class ToolCheck:
    name: str = ""
    min_calls: int = 0
    max_calls: int | None = None

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "ToolCheck":
        return cls(
            name=_as_str(raw.get("name")),
            min_calls=int(raw.get("min_calls", 0)),
            max_calls=_as_int(raw.get("max_calls")),
        )


@dataclass
class ExpectSpec:
    must_contain: list[str] = field(default_factory=list)
    must_not_contain: list[str] = field(default_factory=list)
    regex: str | None = None
    json_schema: str | None = None
    max_steps: int | None = None
    max_seconds: float | None = None
    max_tool_errors: int | None = None
    truncated_ok: bool = False
    files: list[FileCheck] = field(default_factory=list)
    commands: list[CommandCheck] = field(default_factory=list)
    tools: list[ToolCheck] = field(default_factory=list)
    files_unchanged: list[str] = field(default_factory=list)
    forbidden_tools: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "ExpectSpec":
        return cls(
            must_contain=[str(x) for x in _as_list(raw.get("must_contain"))],
            must_not_contain=[str(x) for x in _as_list(raw.get("must_not_contain"))],
            regex=raw.get("regex"),
            json_schema=raw.get("json_schema"),
            max_steps=_as_int(raw.get("max_steps")),
            max_seconds=_as_float(raw.get("max_seconds")),
            max_tool_errors=_as_int(raw.get("max_tool_errors")),
            truncated_ok=_as_bool(raw.get("truncated_ok"), False),
            files=[FileCheck.from_dict(x) for x in _as_list(raw.get("files"))],
            commands=[CommandCheck.from_dict(x) for x in _as_list(raw.get("commands"))],
            tools=[ToolCheck.from_dict(x) for x in _as_list(raw.get("tools"))],
            files_unchanged=[str(x) for x in _as_list(raw.get("files_unchanged"))],
            forbidden_tools=[str(x) for x in _as_list(raw.get("forbidden_tools"))],
        )


@dataclass
class MetricsSpec:
    profile: str = "core"
    use: list[str] = field(default_factory=list)
    disable: list[str] = field(default_factory=list)
    thresholds: dict[str, float] = field(default_factory=dict)
    criteria: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "MetricsSpec":
        thresholds_raw = raw.get("thresholds") or {}
        criteria_raw = raw.get("criteria") or {}
        return cls(
            profile=_as_str(raw.get("profile"), "core"),
            use=[str(x) for x in _as_list(raw.get("use"))],
            disable=[str(x) for x in _as_list(raw.get("disable"))],
            thresholds={str(k): float(v) for k, v in thresholds_raw.items()},
            criteria={str(k): str(v) for k, v in criteria_raw.items()},
        )


@dataclass
class WorkspaceSpec:
    root: str | None = None
    timeout_seconds: float = 300.0
    max_steps: int | None = None
    temperature: float = 0.0
    network: bool = False
    bash: bool = True
    allow_tools: list[str] = field(default_factory=list)
    deny_tools: list[str] = field(default_factory=list)
    keep_on_failure: bool = True
    artifacts: list[ArtifactSpec] = field(default_factory=list)
    setup: list[SetupCommand] = field(default_factory=list)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "WorkspaceSpec":
        return cls(
            root=raw.get("root"),
            timeout_seconds=float(raw.get("timeout_seconds", 300.0)),
            max_steps=_as_int(raw.get("max_steps")),
            temperature=float(raw.get("temperature", 0.0)),
            network=_as_bool(raw.get("network"), False),
            bash=_as_bool(raw.get("bash"), True),
            allow_tools=[str(x) for x in _as_list(raw.get("allow_tools"))],
            deny_tools=[str(x) for x in _as_list(raw.get("deny_tools"))],
            keep_on_failure=_as_bool(raw.get("keep_on_failure"), True),
            artifacts=[ArtifactSpec.from_dict(x) for x in _as_list(raw.get("artifacts"))],
            setup=[SetupCommand.from_dict(x) for x in _as_list(raw.get("setup"))],
        )


@dataclass
class Case:
    id: str
    name: str
    path: Path
    input: str = ""
    expected_output: str = ""
    expected_outcome: str = ""
    expected_tools: list[str] = field(default_factory=list)
    grounding: str = "none"
    context: list[str] = field(default_factory=list)
    retrieval_context: list[str] = field(default_factory=list)
    prompt_instructions: list[str] = field(default_factory=list)
    description: str = ""
    tags: list[str] = field(default_factory=list)
    profile: str = "core"
    difficulty: str = ""
    enabled: bool = True
    workspace: WorkspaceSpec = field(default_factory=WorkspaceSpec)
    expect: ExpectSpec = field(default_factory=ExpectSpec)
    metrics: MetricsSpec = field(default_factory=MetricsSpec)
    checks_module: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    turns: list[dict[str, Any]] = field(default_factory=list)

    @property
    def dir(self) -> Path:
        return self.path.parent

    def threshold(self, metric: str, default: float) -> float:
        return float(self.metrics.thresholds.get(metric, default))

    def artifact_sources(self) -> list[ArtifactSpec]:
        return list(self.workspace.artifacts)


def load_case(path: Path) -> Case:
    """Load one case.toml into a Case without validating metric requirements."""
    path = Path(path)
    try:
        raw = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise CaseError(f"{path}: cannot read TOML: {exc}") from exc

    workspace_raw = raw.get("workspace") or {}
    expect_raw = raw.get("expect") or {}
    metrics_raw = raw.get("metrics") or {}
    checks_raw = raw.get("checks") or {}

    metrics = MetricsSpec.from_dict(metrics_raw)
    profile = _as_str(metrics_raw.get("profile"), _as_str(raw.get("profile"), "core"))
    metrics.profile = profile

    expected_tools = [str(x) for x in _as_list(raw.get("expected_tools"))]
    expect = ExpectSpec.from_dict(expect_raw)
    if not expected_tools:
        expected_tools = [t.name for t in expect.tools if t.name]

    retrieval_context = [str(x) for x in _as_list(raw.get("retrieval_context"))]
    grounding = _as_str(raw.get("grounding"), "static" if retrieval_context else "none")

    case = Case(
        id=_as_str(raw.get("id")),
        name=_as_str(raw.get("name")),
        path=path,
        input=_as_str(raw.get("input")),
        expected_output=_as_str(raw.get("expected_output")),
        expected_outcome=_as_str(raw.get("expected_outcome")),
        expected_tools=expected_tools,
        grounding=grounding,
        context=[str(x) for x in _as_list(raw.get("context"))],
        retrieval_context=retrieval_context,
        prompt_instructions=[str(x) for x in _as_list(raw.get("prompt_instructions"))],
        description=_as_str(raw.get("description")),
        tags=[str(x) for x in _as_list(raw.get("tags"))],
        profile=profile,
        difficulty=_as_str(raw.get("difficulty")),
        enabled=_as_bool(raw.get("enabled"), True),
        workspace=WorkspaceSpec.from_dict(workspace_raw),
        expect=expect,
        metrics=metrics,
        checks_module=checks_raw.get("module"),
        metadata=raw.get("metadata") or {},
        turns=[x for x in _as_list(raw.get("turns")) if isinstance(x, dict)],
    )
    return case


def _resolve_case_path(case: Case, value: str) -> Path:
    return (case.dir / value).resolve()


def _resolve_artifact_source(case: Case, spec: ArtifactSpec) -> Path | None:
    if spec.bundle:
        return (ARTIFACTS_DIR / spec.bundle).resolve()
    if spec.source:
        return _resolve_case_path(case, spec.source)
    return None


def validate_case(case: Case) -> list[str]:
    """Return a list of actionable validation errors for one case."""
    errors: list[str] = []
    prefix = f"{case.id or case.dir.name}"

    if not case.id:
        errors.append(f"{prefix}: missing `id`")
    elif case.id != case.dir.name:
        warnings.warn(
            f"{prefix}: id {case.id!r} does not match directory {case.dir.name!r}",
            stacklevel=2,
        )
    if not case.name:
        errors.append(f"{prefix}: missing `name`")
    if not case.input and not case.turns:
        errors.append(f"{prefix}: missing `input` (or `[[turns]]` for a multi-turn case)")
    if case.turns:
        for index, turn in enumerate(case.turns, start=1):
            role = str(turn.get("role", "")).strip().lower()
            content = turn.get("content")
            if role not in {"user", "assistant"}:
                errors.append(f"{prefix}: turn #{index} role must be 'user' or 'assistant'")
            if not content or not str(content).strip():
                errors.append(f"{prefix}: turn #{index} has empty content")
        if str(case.turns[0].get("role", "")).strip().lower() != "user":
            errors.append(f"{prefix}: the first turn must be a 'user' turn")

    if case.profile not in KNOWN_PROFILES:
        errors.append(f"{prefix}: unknown profile {case.profile!r}; expected one of {sorted(KNOWN_PROFILES)}")
    for key in case.metrics.use + case.metrics.disable:
        if key not in KNOWN_METRICS:
            errors.append(f"{prefix}: unknown metric {key!r}")
    for key, value in case.metrics.thresholds.items():
        if key not in KNOWN_METRICS:
            errors.append(f"{prefix}: threshold for unknown metric {key!r}")
        if not 0.0 <= value <= 1.0:
            errors.append(f"{prefix}: threshold for {key!r} must be between 0 and 1")

    if case.grounding not in KNOWN_GROUNDING:
        errors.append(f"{prefix}: `grounding` must be one of {sorted(KNOWN_GROUNDING)}")

    metric_names = set(case.metrics.use)
    if case.turns:
        # Multi-turn case: conversational metrics only.
        if case.profile == "conversation":
            metric_names.update({"conversation_completeness", "turn_relevancy", "conversational_correctness"})
        metric_names.difference_update(case.metrics.disable)
        bad = metric_names & SINGLE_TURN_METRICS
        if bad:
            errors.append(f"{prefix}: multi-turn cases cannot use single-turn metrics: {sorted(bad)}")
        if not metric_names & CONVERSATIONAL_METRICS:
            errors.append(f"{prefix}: multi-turn case needs at least one conversational metric (profile = \"conversation\")")
        if metric_names & {"conversation_completeness", "conversational_correctness"} and not case.expected_outcome:
            errors.append(f"{prefix}: conversational outcome metrics need `expected_outcome`")
    else:
        if case.profile in {"core", "tools", "code", "docs", "format"}:
            metric_names.update({"task_completion", "step_efficiency", "correctness"})
        if case.profile == "full":
            metric_names.update({
                "task_completion", "step_efficiency", "correctness",
                "answer_relevancy", "argument_correctness",
                "bias", "toxicity", "pii_leakage",
            })
            if case.expected_tools:
                metric_names.add("tool_correctness")
            if case.workspace.root or case.workspace.artifacts:
                metric_names.add("code_change_quality")
            if case.retrieval_context or case.grounding == "tool_outputs":
                metric_names.update({"faithfulness", "contextual_relevancy"})
            if case.prompt_instructions:
                metric_names.add("prompt_alignment")
        if case.profile == "tools":
            metric_names.update({"tool_correctness", "argument_correctness"})
        if case.profile == "docs":
            metric_names.update({"faithfulness", "contextual_relevancy"})
        if case.profile == "code":
            metric_names.add("code_change_quality")
        if case.profile == "format":
            metric_names.add("prompt_alignment")
        if case.profile == "safety":
            metric_names.update({"bias", "toxicity", "pii_leakage"})
        if case.profile == "conversation":
            errors.append(f"{prefix}: profile \"conversation\" requires `[[turns]]`")
        metric_names.difference_update(case.metrics.disable)

        if "correctness" in metric_names or "code_change_quality" in metric_names:
            if not case.expected_output:
                errors.append(f"{prefix}: `{sorted(metric_names & {'correctness', 'code_change_quality'})}` needs `expected_output`")
        if "tool_correctness" in metric_names and not case.expected_tools:
            errors.append(f"{prefix}: `tool_correctness` needs `expected_tools` or [[expect.tools]]")
        if metric_names & {"faithfulness", "contextual_relevancy"}:
            if not case.retrieval_context and case.grounding != "tool_outputs":
                errors.append(
                    f"{prefix}: grounding metrics need `retrieval_context` or `grounding = \"tool_outputs\"`"
                )
        if "prompt_alignment" in metric_names and not case.prompt_instructions:
            errors.append(f"{prefix}: `prompt_alignment` needs `prompt_instructions`")

    # Tool policy and expectations.
    for name in case.workspace.allow_tools + case.workspace.deny_tools + case.expected_tools + case.expect.forbidden_tools:
        if name not in TOOL_NAMES:
            errors.append(f"{prefix}: unknown tool {name!r}")
    overlap = set(case.workspace.allow_tools) & set(case.workspace.deny_tools)
    if overlap:
        errors.append(f"{prefix}: tools both allowed and denied: {sorted(overlap)}")
    if not case.workspace.bash and "bash" in case.workspace.allow_tools:
        errors.append(f"{prefix}: `bash` is disabled but listed in `allow_tools`")
    if not case.workspace.network:
        for name in case.workspace.allow_tools:
            if name in {"web_search", "fetch_url"}:
                errors.append(f"{prefix}: `{name}` needs `network = true`")
        if "web_search" in case.expected_tools or "fetch_url" in case.expected_tools:
            errors.append(f"{prefix}: expected network tool but `network = false`")

    # Workspace root and artifacts.
    if case.workspace.root:
        root = _resolve_case_path(case, case.workspace.root)
        if not root.exists():
            errors.append(f"{prefix}: workspace.root does not exist: {root}")
    for index, spec in enumerate(case.workspace.artifacts, start=1):
        label = f"{prefix} artifact #{index}"
        if spec.kind not in KNOWN_ARTIFACT_KINDS:
            errors.append(f"{label}: unknown kind {spec.kind!r}")
        if spec.transform not in KNOWN_TRANSFORMS:
            errors.append(f"{label}: unknown transform {spec.transform!r}")
        if spec.mode not in {"copy", "symlink"}:
            errors.append(f"{label}: mode must be copy or symlink")
        if not spec.target:
            errors.append(f"{label}: missing target")
        if spec.kind == "inline":
            if spec.content is None:
                errors.append(f"{label}: inline kind needs `content`")
            if spec.target in {"", "."} or spec.target.endswith("/"):
                errors.append(
                    f"{label}: inline kind needs a file `target` (for example NOTES.md)"
                )
        elif spec.kind == "url":
            if not spec.source:
                errors.append(f"{label}: url kind needs `source`")
            if not (spec.network or case.workspace.network):
                errors.append(f"{label}: url kind needs `network = true`")
        else:
            if bool(spec.source) == bool(spec.bundle):
                errors.append(f"{label}: set exactly one of `source` or `bundle`")
            else:
                source = _resolve_artifact_source(case, spec)
                if source is not None and not source.exists():
                    errors.append(f"{label}: source does not exist: {source}")
            if spec.mode == "symlink" and spec.transform != "copy":
                errors.append(f"{label}: symlink mode cannot use transform {spec.transform!r}")

    for index, setup in enumerate(case.workspace.setup, start=1):
        if not setup.command.strip():
            errors.append(f"{prefix} setup #{index}: empty command")

    for index, file_check in enumerate(case.expect.files, start=1):
        if not file_check.path:
            errors.append(f"{prefix} file check #{index}: missing path")
    for index, command in enumerate(case.expect.commands, start=1):
        if not command.command.strip():
            errors.append(f"{prefix} command check #{index}: empty command")
    for index, tool in enumerate(case.expect.tools, start=1):
        if tool.name not in TOOL_NAMES:
            errors.append(f"{prefix} tool check #{index}: unknown tool {tool.name!r}")
        if tool.max_calls is not None and tool.max_calls < tool.min_calls:
            errors.append(f"{prefix} tool check #{index}: max_calls < min_calls")

    if case.expect.json_schema:
        schema_path = _resolve_case_path(case, case.expect.json_schema)
        if not schema_path.is_file():
            errors.append(f"{prefix}: json_schema does not exist: {schema_path}")
    if case.checks_module:
        checks_path = _resolve_case_path(case, case.checks_module)
        if not checks_path.is_file():
            errors.append(f"{prefix}: checks module does not exist: {checks_path}")

    return errors


def discover_cases(
    *,
    include_disabled: bool = False,
    strict: bool = True,
    cases_dir: Path | None = None,
) -> list[Case]:
    """Discover cases from disk and apply EVAL_CASES / EVAL_TAG / EVAL_PROFILE filters."""
    root = Path(cases_dir or CASES_DIR)
    include_disabled = include_disabled or os.getenv(
        "EVAL_INCLUDE_DISABLED", ""
    ).strip().lower() in {"1", "true", "yes"}
    cases: list[Case] = []
    errors: list[str] = []
    for path in sorted(root.glob("*/case.toml")):
        try:
            case = load_case(path)
        except CaseError as exc:
            errors.append(str(exc))
            continue
        if not include_disabled and not case.enabled:
            continue
        case_errors = validate_case(case)
        if strict:
            errors.extend(case_errors)
        cases.append(case)

    if errors:
        raise CaseError("\n".join(errors))

    ids = {x.strip() for x in os.getenv("EVAL_CASES", "").split(",") if x.strip()}
    tag = os.getenv("EVAL_TAG", "").strip()
    profile = os.getenv("EVAL_PROFILE", "").strip()
    if ids:
        cases = [c for c in cases if c.id in ids]
    if tag:
        cases = [c for c in cases if tag in c.tags]
    if profile:
        cases = [c for c in cases if c.profile == profile]
    return cases
