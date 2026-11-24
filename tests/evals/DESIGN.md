# Agent Evaluation System — Design v1

> **Current status:** the registry, metric profiles, fallback judge and both
> suites were rebuilt. `README.md` is the source of truth for the current
> setup (LLM-only verdicts, multi-turn enabled, 12 cases). This document is
> retained for the harness architecture and rationale; its "Phase 2" notes
> about multi-turn are superseded.

**Status:** implemented (Phase 1) in this directory; application code unchanged  
**Target:** the `context_agent` text-to-text, tool-using agent (`agent.py`, `context_agent/cli.py`)  
**Date:** 2026-11-19  
**DeepEval:** 4.3.4 (verified in this environment)

---

## 0. TL;DR

We will add a **case registry** under `tests/evals/`:

- A **case** is a directory containing a `case.toml`, optional `artifacts/`, optional `checks.py`, and optional expected files.
- A case declares its **input**, **expected text**, **expected tools**, **metrics profile**, **artifact attachments**, and **deterministic checks**.
- A small harness **materializes a fresh sandbox**, runs the real `IntelligentAgent`, records tool calls, emits DeepEval traces, runs deterministic checks, then runs DeepEval LLM metrics on the final text.
- Adding a case = add a directory. Removing a case = delete the directory or set `enabled = false`. No central registry file to edit.
- A case can attach a **codebase**, **documents**, **CSV/data**, **HTML**, **PDF**, **inline text**, or a shared **artifact bundle**, each with its own target path and transform.
- The application code is **not modified**. Instrumentation is done with subclasses/wrappers owned by the eval harness.

Two eval shapes are supported:

1. **Single-turn agentic E2E (default):** one task, traced, deterministic side-effect checks + LLM judges.
2. **Multi-turn conversation (phase 2):** scripted turns or `ConversationSimulator`, using only multi-turn metrics.

---

## 1. What we are evaluating (code-derived facts)

### 1.1 Entry points

| Entry | File | Notes |
|---|---|---|
| `main()` | `context_agent/cli.py` | argparse CLI, `--query` for one query and exit |
| `IntelligentAgent.process_query(text, on_token=None)` | `context_agent/agent.py` | returns the final assistant text; catches `LLMError` and generic exceptions into text |
| `IntelligentAgent._run_turn()` | `context_agent/agent.py` | model/tool loop, up to `max_steps_per_turn` (default 25) |
| `Toolbox.run(name, args, cap)` | `context_agent/tools/registry.py` | single dispatch point for every tool call |
| `SessionStore` | `context_agent/storage/session_store.py` | `transcript.jsonl`, `state.json`, `spill/` |

### 1.2 Runtime facts that shape the eval design

- **Tools available:** `read_file`, `write_file`, `edit_file`, `search_text`, `search_files`, `list_files`, `bash`, `web_search`, `fetch_url`, `update_plan`, `save_note`.
- **The agent loop is bounded:** `Config.max_steps_per_turn = 25`; loop guard at `loop_warn=3`, `loop_stop=5`.
- **Session state is persistent:** history, working state, file tracker, summary, notes, saved outputs, and token calibration all live in the session store.
- **Paths are process-CWD relative:** `ToolExecutionContext.resolve()` uses `os.path.abspath(...)`; `bash` defaults to `cwd="."`. A sandbox must change the process working directory during a run.
- **Bash is unrestricted:** it runs with the user's permissions and `start_new_session=True`. The workspace is an **isolation convenience**, not a security boundary.
- **Tool output is bounded:** `max_tool_chars=5000`; oversized output is spilled to `spill/` and the model sees a head/tail plus a path.
- **Final answers can be infrastructure errors:** `process_query` converts `LLMError` into `"Model error: ..."` and unexpected exceptions into `"Internal error (...)"`. Evals must classify these as **infrastructure failures**, not judge them as answers.
- **Final answers can be truncated:** step-limit and loop-guard wrap-ups append text such as `"Stopped early: step limit reached"` or `"the same call kept repeating without progress"`.
- **No native trace hook exists:** the cleanest instrumentation point is `Toolbox.run` (subclass) and `IntelligentAgent._chat` (optional LLM spans).

### 1.3 Use-case classification

Per the DeepEval skill's precedence (`chatbot / multi-turn agent > agent > RAG`), this app is primarily an **agent**: it uses tools, plans, edits files, and runs commands. It is also stateful (a chat session), so multi-turn behavior is a real but **secondary** eval surface.

**Primary shape:** single-turn agentic E2E with traces.  
**Secondary shape:** multi-turn conversation E2E with conversational metrics.

The final artifact under test is **text-to-text**: a user input produces a final assistant text. Because the agent acts through tools, we also score the **behavior** (tools, arguments, steps) and **side effects** (files, commands), not only the text.

---

## 2. Goals and non-goals

### Goals

1. A reusable benchmark for the agent using generic agent metrics:
   - task completion
   - step efficiency
   - tool correctness
   - argument correctness
   - answer correctness (custom `GEval` against an expected output)
   - grounding/faithfulness for document cases
   - optional safety metrics
2. **Per-case artifacts:** a case can attach a repo, documents, data files, HTML, PDFs, or inline text.
3. **Add/remove without code:** a case is a directory; tags and profiles select subsets.
4. **Deterministic expectations:** file state, command exit codes, output substrings/regex, forbidden tools, step/time budgets.
5. **Reproducible sandbox:** fresh workspace, fresh agent session, fresh `Config.home` per case.
6. **Inspectable traces:** tool spans, final output, expected output, and metric scores are visible in DeepEval / Confident AI.
7. **CI-friendly:** runnable with `deepeval test run`; raw `pytest` skips the eval subtree.

### Non-goals (v1)

- Changing agent behavior or prompts.
- Production monitoring or online evals.
- Training or fine-tuning.
- A web UI or dashboard of our own.
- A hard security sandbox for untrusted code (Docker is a later phase).

---

## 3. Design principles

1. **Registry over monolith.** Cases are discovered from disk; there is no central list to edit.
2. **The case owns its data, expectations, and metric selection.** The harness is generic.
3. **Deterministic checks first, LLM judges second.** Exact file/command/output checks catch regressions cheaply; LLM metrics judge semantic correctness.
4. **Trace the real run.** Use DeepEval `@observe` + tool spans; do not hand-build an `LLMTestCase` for the traced single-turn path.
5. **Fresh everything.** New workspace, new `Config.home`, new `IntelligentAgent` per case. Multi-turn cases reuse one agent deliberately.
6. **The app stays clean.** All tracing/recording lives in `tests/evals/harness/`.
7. **Fail fast on invalid cases.** `evalctl validate` catches missing fields before a model is called.
8. **Curated cases + generated cases.** Curated artifact cases cover deep agent behavior; generated docs cases provide breadth.
9. **Record the environment.** Model, provider, endpoint, DeepEval version, artifact hashes, git commit, and timestamps go into the report.

---

## 4. Repository layout

```text
tests/
  evals/
    DESIGN.md                     # this document
    README.md                     # user-facing quick start (phase 1)
    __init__.py                   # makes tests.evals importable
    conftest.py                   # skip evals under raw pytest unless DEEPEVAL is set
    metrics.py                    # metric factories + profiles (the only metric edit point)
    test_agent_eval.py            # single-turn traced suite, parametrized over cases
    test_agent_conversation.py    # phase 2: multi-turn suite
    harness/
      __init__.py
      case.py                     # Case dataclasses, TOML loading, discovery, validation
      workspace.py                # sandbox, artifact materialization, transforms, snapshot/diff
      recorder.py                 # RecordingToolbox, RunRecorder, EvalAgent
      runner.py                   # run_traced_case(), deterministic checks, orchestration
      serving.py                  # Google AI Studio chain, rate-limit fallback, Ollama safety net
      checks.py                   # built-in deterministic check implementations
      judge.py                    # DeepEval judge model factory (Ollama / local / API)
      report.py                   # per-case artifacts + summary.json/md
      cli.py                      # evalctl: list/validate/run/new/export/import/report
    cases/
      metrics-demo-001/
        case.toml                 # disabled demo of the full metric profile
      <case-id>/                  # add your own with `evalctl new`
        case.toml
        artifacts/
          repo/                   # attached codebase
        expected/
          schema.json             # optional JSON schema
        checks.py                 # optional custom deterministic checks
    artifacts/                    # shared, reusable bundles
      product-docs/
      legacy-repo/
    .runs/                        # generated reports (gitignored)
    .cache/                       # transformed artifacts (gitignored)
    .dataset.json                 # generated DeepEval export (optional, gitignored or committed)
```

**Why the test file is parametrized over cases, not over `.dataset.json`:** a standard `Golden` cannot carry a sandbox/artifact bundle. The registry is the human-editable source of truth; `.dataset.json` is a generated export for DeepEval/Confident AI sharing. Each case still produces a real `Golden` at runtime, so all DeepEval metrics work normally.

---

## 5. Case manifest — the extension point

### 5.1 Minimal case

```toml
# tests/evals/cases/my-text-case/case.toml
id = "my-text-case"
name = "Explain a failing HTTP 502"
enabled = true
tags = ["core", "reasoning"]
profile = "core"

input = """
A service returns HTTP 502 from its reverse proxy, but the upstream process is
healthy on localhost:8080. List the three most likely causes and the first
diagnostic command you would run for each.
"""

expected_output = """
Likely causes: proxy/upstream port mismatch, upstream timeout before headers,
or a proxy/upstream protocol mismatch. Diagnostics: curl localhost:8080,
inspect proxy error log/timeouts, verify the proxy upstream address and scheme.
"""
```

### 5.2 Full schema

```toml
id = "my-code-case"                 # required, slug, should match directory name
name = "Fix the off-by-one in calc" # required, human label
description = "..."                 # optional
enabled = true                      # default true; false excludes it from discovery
tags = ["code", "tool-use"]         # used by `evalctl run --tag`
profile = "code"                    # optional default metric profile
difficulty = "medium"               # optional metadata

input = """..."""                   # required for single-turn
expected_output = """..."""         # required by correctness-style metrics
expected_outcome = """..."""        # optional natural-language outcome (multi-turn)
expected_tools = ["read_file"]      # optional; derived from [[expect.tools]] if omitted
grounding = "tool_outputs"          # tool_outputs | static | none (see §7.4)

# Static context / grounding, if the case provides it directly.
context = ["..."]                   # optional
retrieval_context = ["..."]         # optional; static docs excerpts

# ---------------------------------------------------------------- workspace
[workspace]
# Optional convenience: copy this tree to the workspace root before artifacts.
root = "artifacts/repo"
timeout_seconds = 300               # wall-clock cap for the agent run
max_steps = 20                      # overrides Config.max_steps_per_turn
temperature = 0.0                   # default 0.0 for evals
network = false                     # hides web_search/fetch_url when false
bash = true                         # false removes the bash tool
allow_tools = []                    # if non-empty, only these tools are exposed
deny_tools = ["web_search", "fetch_url"]
keep_on_failure = true              # preserve the workspace in .runs for debugging

# Each artifact is copied/materialized into the sandbox.
[[workspace.artifacts]]
kind = "repo"                       # repo | docs | file | inline | url
source = "artifacts/repo"           # relative to the case directory
target = "."                        # relative to the workspace root
mode = "copy"                       # copy | symlink
exclude = [".git", "node_modules", "__pycache__", ".DS_Store"]
transform = "copy"                  # copy | text | html_to_text | pdf_to_text | csv_to_markdown | unpack

[[workspace.artifacts]]
kind = "docs"
bundle = "product-docs"             # resolved from tests/evals/artifacts/
target = "docs"
transform = "html_to_text"
include = ["*.html", "*.md"]

[[workspace.artifacts]]
kind = "file"
source = "artifacts/data/sales.csv"
target = "data/sales.csv"
transform = "csv_to_markdown"

[[workspace.artifacts]]
kind = "inline"
target = "TASK.md"
content = """Extra instructions or seed notes can be written directly."""

# Optional setup commands, run before the agent.
[[workspace.setup]]
command = "git init -q && git add . && git -c user.email=eval@local -c user.name=eval commit -qm baseline"
cwd = "."
timeout = 30
optional = false

# ---------------------------------------------------------------- expectations
[expect]
must_contain = ["return a + b"]     # final answer checks
must_not_contain = ["I cannot"]
regex = "..."                       # optional
json_schema = "expected/schema.json" # optional, relative to case dir
max_steps = 15                      # overrides workspace.max_steps
max_seconds = 120
max_tool_errors = 0                 # failed tool calls allowed
truncated_ok = false                # fail if the agent hit the step/loop guard

[[expect.files]]
path = "repo/calc.py"               # relative to workspace root
exists = true
contains = ["return a + b"]
not_contains = ["return a - b"]
regex = "..."
sha256 = "..."                      # optional exact hash
min_bytes = 1
max_bytes = 100000

[[expect.commands]]
command = "python -m pytest -q"
cwd = "repo"
exit_code = 0
contains = ["1 passed"]
not_contains = ["FAILED"]
timeout = 120

[[expect.tools]]
name = "read_file"
min_calls = 1
max_calls = 10

[[expect.tools]]
name = "edit_file"
min_calls = 1

# Optional custom checks. The module exposes check(ctx) -> list[CheckResult].
[checks]
module = "checks.py"

# ---------------------------------------------------------------- metrics
[metrics]
use = ["task_completion", "step_efficiency", "correctness", "tool_correctness", "argument_correctness"]
disable = ["answer_relevancy"]
# Per-metric threshold overrides.
[metrics.thresholds]
task_completion = 0.8
step_efficiency = 0.6
correctness = 0.7
tool_correctness = 0.9
argument_correctness = 0.8

[metadata]
owner = "rudram"
source = "curated"                  # curated | generated | imported
```

### 5.3 What each artifact kind means

| Kind | Source | Best for | Notes |
|---|---|---|---|
| `repo` | directory | codebase tasks | copy or symlink; excludes VCS/junk dirs |
| `docs` | directory or bundle | documentation QA/grounding | mixed `.md`, `.txt`, `.html`, `.pdf`, `.csv` with transforms |
| `file` | single file | one CSV/JSON/PDF/HTML | can rename via `target` |
| `inline` | literal content | small seeds, task notes | no external file needed |
| `url` | http(s) | snapshotting a live page | opt-in `network = true`; content hash recorded |

**Shared bundles** live in `tests/evals/artifacts/<name>/`. A case references `bundle = "<name>"` instead of `source = "..."`. This is how several cases reuse the same docs corpus or repo without copying it.

**Artifact transforms** are explicit and cached:

| Transform | Behavior |
|---|---|
| `copy` | verbatim copy (default) |
| `text` | decode text, normalize newlines/encoding |
| `html_to_text` | strip HTML into readable text using the agent's own `HtmlTextExtractor` |
| `pdf_to_text` | convert PDF to text if `pypdf` is installed; otherwise fail with an actionable message |
| `csv_to_markdown` | convert CSV into a markdown table (no extra dependency) |
| `unpack` | unpack `.zip`/`.tar` into the target directory |

Transformed output is materialized directly into each sandbox in Phase 1. A
content-addressed cache under `tests/evals/.cache/artifacts/` (keyed by source
hash + transform + version) is planned as an optimization and does not change
case semantics. The workspace manifest records hashes of the materialized files,
so a run is reproducible. **Prefer committing plain-text artifacts** when
possible; transforms are a convenience, not a requirement.

### 5.4 Example: codebase case

```toml
id = "my-code-case"
name = "Fix the failing calculator test"
enabled = true
tags = ["code", "tool-use", "core"]
profile = "code"

input = """
The repository in `./repo` has a failing test. Find the bug, fix it, and run the
test suite. Report the root cause and the exact change you made.
"""

expected_output = """
The `add` function subtracts instead of adding. It should return `a + b`.
The test suite passes after the fix.
"""

[workspace]
root = "artifacts/repo"
network = false
bash = true
max_steps = 20

[[workspace.artifacts]]
kind = "repo"
source = "artifacts/repo"
target = "."

[expect]
max_steps = 15
truncated_ok = false

[[expect.files]]
path = "calc.py"
contains = ["return a + b"]
not_contains = ["return a - b"]

[[expect.commands]]
command = "python -m pytest -q"
cwd = "."
exit_code = 0

[[expect.tools]]
name = "read_file"
min_calls = 1

[[expect.tools]]
name = "edit_file"
min_calls = 1

[[expect.tools]]
name = "bash"
min_calls = 1

[metrics]
use = ["task_completion", "step_efficiency", "correctness", "tool_correctness", "argument_correctness"]
```

### 5.5 Example: multi-document case

```toml
id = "my-docs-case"
name = "Answer from the product handbook"
enabled = true
tags = ["docs", "grounding"]
profile = "docs"

input = """
Using the documents in `./docs`, what is the refund window for annual plans,
and which document states it? Cite the document name.
"""
expected_output = """
Annual plans can be refunded within 30 days of purchase. This is stated in
`billing-policy.md` (section "Annual plans").
"""
grounding = "tool_outputs"

[workspace]
root = "."
network = false
bash = false

[[workspace.artifacts]]
kind = "docs"
bundle = "product-docs"
target = "docs"
transform = "html_to_text"
include = ["*.html", "*.md", "*.pdf"]

[metrics]
use = ["task_completion", "correctness", "faithfulness", "contextual_relevancy"]
[metrics.thresholds]
faithfulness = 0.8
contextual_relevancy = 0.7
```

For grounding metrics, the runner builds `retrieval_context` from the tool outputs the agent actually read (`read_file`, `search_text`, `fetch_url`), de-duplicated and clipped. If the case provides static `retrieval_context`, that is used instead. Validation rejects `faithfulness`/`contextual_relevancy` if neither source exists.

### 5.6 Example: no-artifact case

```toml
id = "my-text-case"
name = "Explain a failing HTTP 502"
enabled = true
tags = ["core", "reasoning"]
profile = "core"

input = """..."""
expected_output = """..."""

[workspace]
network = false
bash = false

[metrics]
use = ["task_completion", "step_efficiency", "correctness", "answer_relevancy"]
```

---

## 6. Execution pipeline

```text
discover cases
      |
      v
validate manifest + metric requirements
      |
      v
create temp workspace  <-- copy artifacts / bundles / transforms
      |
      v
run setup commands (optional)
      |
      v
snapshot workspace (hash manifest)
      |
      v
fresh Config(home=temp) + fresh EvalAgent
      |
      v
@observe(agent) run: chdir(workspace), process_query(...)
      |         |
      |         +--> RecordingToolbox -> tool spans + ToolCallRecords
      |
      v
restore cwd, snapshot diff, collect transcript/tool calls/final text
      |
      v
deterministic checks (files, commands, output, tools, budgets, custom checks)
      |
      v
update_current_trace(expected_output, context, retrieval_context, tools_called)
      |
      v
assert_test(golden=..., metrics=case_metrics)
      |
      v
write report (summary, transcript, tool calls, diff, checks, scores)
      |
      v
cleanup or preserve workspace on failure
```

### 6.1 Discovery and validation

`discover_cases()` walks `tests/evals/cases/*/case.toml`, loads each manifest, resolves defaults, and filters `enabled`. A case's `id` must match its directory name (warn otherwise).

Validation fails fast for:

- missing `id`, `name`, or `input`
- unknown profile or metric name
- `correctness` without `expected_output`
- `tool_correctness` without `expected_tools` (from `expect.tools` or an explicit list)
- `faithfulness`/`contextual_relevancy` without static or captured retrieval context
- artifact `source` missing, or both/neither `source` and `bundle`
- `json_schema` file missing
- `checks.module` missing, not importable, or lacking `check(ctx)`
- duplicate case ids

`evalctl validate` prints a table of case, profile, metrics, artifacts, and errors. The pytest suite also validates at import time so a bad case fails with a clear message rather than a model call.

### 6.2 Sandbox and working directory

- Create `tempfile.mkdtemp(prefix="agenteval-<case>-")` outside the repo.
- Workspace root: `<temp>/workspace`.
- Agent home: `<temp>/agent_home` (not inside the workspace) so session files never pollute the case repo.
- `os.chdir(workspace)` around the agent run; restore in `finally`.
- Snapshot the behavioral workspace diff **immediately after the agent run and before `[[expect.commands]]`**, so test commands do not pollute the diff.
- `Config(home=agent_home, verbose=False, temperature=0.0, ...)`.
- Per-case `max_steps`, `timeout`.
- The workspace is not a security boundary; see §12.

### 6.3 Agent wrapper (no app edits)

```python
# tests/evals/harness/recorder.py
from context_agent.agent import IntelligentAgent
from context_agent.tools.registry import Toolbox
from deepeval.tracing import observe, update_current_span


def make_traced_runner(toolbox):
    # The closure avoids passing the non-serializable toolbox as an @observe
    # argument; the span gets only the tool name, args, and output.
    @observe(type="tool")
    def run(name, args, cap):
        result = Toolbox.run(toolbox, name, args, cap)
        update_current_span(
            name=name,
            input=args,
            output=result.text,
            metadata={"ok": result.ok, **result.meta},
        )
        return result

    return run


class RecordingToolbox(Toolbox):
    def __init__(self, *args, recorder, policy, **kwargs):
        super().__init__(*args, **kwargs)
        self.recorder = recorder
        self.policy = policy
        # Expose only the allowed tools to the model.
        self.schemas = [s for s in self.schemas
                        if self.policy.allows(s["function"]["name"])]
        self._handlers = {k: v for k, v in self._handlers.items()
                          if self.policy.allows(k)}
        self._traced_run = make_traced_runner(self)

    def run(self, name, args, cap):
        result = self._traced_run(name, args, cap)
        self.recorder.record(name, args, result)
        return result


class EvalAgent(IntelligentAgent):
    def __init__(self, cfg, recorder, policy, **kwargs):
        super().__init__(cfg, **kwargs)
        # ContextManager only uses schemas for a token estimate, so replacing
        # the toolbox after construction is safe.
        self.tools = RecordingToolbox(
            self.cfg, self.files, self.state, self.store,
            recorder=recorder, policy=policy,
        )
```

> **Validated detail (spike):** `next_tool_span(...)` does **not** create a
> span. It only stages default fields for the next span that some integration
> creates. Using it as a `with` block around a hand-written tool call attaches
> the tool output to the *parent* agent span. The correct pattern is
> `@observe(type="tool")` on the tool wrapper, then `update_current_span(...)`
> inside it. A local spike with DeepEval 4.3.4 produced this trace shape:
>
> ```json
> {"name": "run_agent", "type": "agent", "output": "final text",
>  "children": [{"name": "read_file", "type": "tool",
>                "input": {"path": "x"}, "output": "file body"}]}
> ```
>
> The same spike confirmed that `expected_output`, `tools_called`,
> `expected_tools`, `context`, and `retrieval_context` reach a trace-scoped
> metric through `assert_test(golden=...)`.

Tool filtering is deliberately implemented in the harness, not the app. A `ToolPolicy` supports `allow_tools`, `deny_tools`, `network`, and `bash`. Denied tools are removed from both the advertised schema and the handler map, so the model cannot call them.

### 6.4 Run and trace

```python
# tests/evals/harness/runner.py
from deepeval.tracing import observe, update_current_trace
from deepeval.test_case import ToolCall

@observe(type="agent", name=case.id)
def run_traced_case(case, workspace):
    update_current_trace(
        name=case.id,
        tags=case.tags,
        metadata={...},
        input=case.input,
        expected_output=case.expected_output,
        context=case.context or None,
        retrieval_context=case.retrieval_context or None,
        expected_tools=[ToolCall(name=n) for n in case.expected_tools] or None,
    )
    result = run_agent(case, workspace)
    update_current_trace(
        output=result.final_output,
        tools_called=[
            ToolCall(name=r.name, input_parameters=r.args, output=r.output)
            for r in result.tool_calls
        ],
        retrieval_context=result.retrieval_context or None,
    )
    return result.final_output
```

Why `update_current_trace(...)` matters (verified in DeepEval 4.3.4):

- `assert_test(golden=...)` requires an active trace created by `@observe` inside a `deepeval test run`.
- The trace-level test case reads `expected_output`, `context`, `retrieval_context`, `tools_called`, and `expected_tools` from the active trace (with a fallback to the `Golden` for metrics).
- `StepEfficiencyMetric` reads `test_case._trace_dict`, which is populated from the trace spans. Without tool spans, it has nothing useful to judge.
- `ToolCorrectnessMetric` requires `tools_called` and `expected_tools`; `ArgumentCorrectnessMetric` requires `tools_called`.

### 6.5 Test shape

```python
# tests/evals/test_agent_eval.py
import pytest
from deepeval import assert_test

from tests.evals.harness.case import discover_cases
from tests.evals.harness.checks import evaluate_checks
from tests.evals.harness.report import write_report
from tests.evals.harness.runner import make_golden, run_traced_case
from tests.evals.harness.workspace import create_workspace
from tests.evals.metrics import metrics_for

CASES = discover_cases()

@pytest.mark.parametrize("case", CASES, ids=[c.id for c in CASES])
def test_agent_case(case):
    with create_workspace(case) as ws:                 # fresh sandbox + artifacts
        result = run_traced_case(case, ws)             # emits the agent trace
        checks = evaluate_checks(case, result, ws)     # deterministic checks
        metrics = metrics_for(case, result)            # profile -> metric objects
        metric_error = None
        try:
            assert_test(
                golden=make_golden(case, result, checks),
                metrics=metrics,
            )
        except AssertionError as exc:
            metric_error = exc
        write_report(case, result, checks, metrics=metrics, metric_error=metric_error)
        if checks.failures or metric_error:
            raise AssertionError(combine(checks, metric_error))
```

Both failure sources are reported together. A deterministic failure does not hide the LLM scores, and an LLM failure does not hide the file/command evidence.

### 6.6 Deterministic checks

Built-in checks:

- **Output:** `must_contain`, `must_not_contain`, regex, JSON schema, max length.
- **Files:** exists, contains/not-contains, regex, exact SHA-256, size bounds.
- **Commands:** run after the agent, assert exit code and output substrings.
- **Tools:** expected names, min/max call counts, forbidden tools, max failed tool calls.
- **Budgets:** max steps, max seconds, no truncation unless allowed.
- **Workspace:** added/modified/deleted manifest; optionally assert specific files are unchanged.
- **Infrastructure:** detect `"Model error:"`, `"Internal error ("`, empty responses, startup failures; mark the case as an infra failure rather than a model-quality failure.

**Custom checks escape hatch:** a case can include `checks.py`:

```python
# tests/evals/cases/my-code-case/checks.py
from tests.evals.harness.checks import CheckResult

def check(ctx):
    diff = ctx.diff
    return [
        CheckResult("only_expected_file_changed",
                    set(diff.modified) <= {"calc.py"},
                    f"modified={sorted(diff.modified)}"),
        CheckResult("no_large_output",
                    len(ctx.final_output) < 4000,
                    f"chars={len(ctx.final_output)}"),
    ]
```

`ctx` exposes `final_output`, `tool_calls`, `workspace`, `diff`, `history`, `checks`, `run`, and `case`. This keeps complex assertions local to the case without growing the harness.

### 6.7 Reporting

Every case writes to `tests/evals/.runs/<run_id>/<case_id>/`:

- `case.toml` snapshot
- `workspace_manifest_before.json`
- `workspace_diff.json` (added/modified/deleted + hashes)
- `transcript.jsonl` (copied from the agent's session store)
- `tool_calls.json`
- `final.md`
- `checks.json`
- `metrics.json` (scores parsed from DeepEval's run data, when available)
- `workspace/` only if the case failed and `keep_on_failure = true`

`summary.json` and `summary.md` at the run root contain one row per case: pass/fail, metric scores, steps, seconds, tool errors, artifact hashes, model, provider, DeepEval version, and git commit. This is the benchmark artifact.

---

## 7. Metrics and profiles

### 7.1 Metric catalog

| Key | DeepEval metric | Required fields | What it answers |
|---|---|---|---|
| `task_completion` | `TaskCompletionMetric` | input, actual_output, trace | Did the agent complete the task? |
| `step_efficiency` | `StepEfficiencyMetric` | input, actual_output, trace | Did it use a reasonable number of steps/tools? |
| `correctness` | custom `GEval` | input, actual_output, expected_output | Does the final text match the expected result semantically? |
| `code_change_quality` | custom `GEval` | input, actual_output, expected_output, context (diff/tests) | Is the code change correct and minimal? |
| `answer_relevancy` | `AnswerRelevancyMetric` | input, actual_output | Is the answer on-topic? |
| `tool_correctness` | `ToolCorrectnessMetric` | input, tools_called, expected_tools | Did it use the right tools? |
| `argument_correctness` | `ArgumentCorrectnessMetric` | input, tools_called | Are tool arguments sensible/correct? |
| `faithfulness` | `FaithfulnessMetric` | input, actual_output, retrieval_context | Is the answer grounded in what it read? |
| `contextual_relevancy` | `ContextualRelevancyMetric` | input, retrieval_context | Was the retrieved/read context relevant? |
| `plan_adherence` | `PlanAdherenceMetric` | input, actual_output, trace | Did it follow its plan? (optional) |
| `plan_quality` | `PlanQualityMetric` | input, actual_output, trace | Was the plan good? (optional) |
| `json_correctness` | `JsonCorrectnessMetric` | input, actual_output, schema | Structured output validity (phase 2; v1 uses the deterministic `expect.json_schema` check) |
| `prompt_alignment` | `PromptAlignmentMetric` | input, actual_output, instructions | Did it follow formatting/instruction constraints? |
| `bias` | `BiasMetric` | input, actual_output | Optional safety |
| `toxicity` | `ToxicityMetric` | input, actual_output | Optional safety |
| `pii_leakage` | `PIILeakageMetric` | input, actual_output | Optional safety |
| `conversation_completeness` | `ConversationCompletenessMetric` | turns | Multi-turn: did the conversation reach the outcome? |
| `turn_relevancy` | `TurnRelevancyMetric` | turns | Multi-turn: are turns relevant? |
| `conversational_correctness` | `ConversationalGEval` | turns | Multi-turn custom criterion |

### 7.2 Profiles

Profiles are named metric bundles. A case selects one with `profile = "..."` and can `use`/`disable` individual metrics. Semantics: the profile supplies defaults, `use` adds metrics, `disable` removes them, and `profile = "none"` starts from an empty set. This makes a profile a baseline rather than a lock-in.

| Profile | Metrics | Use for |
|---|---|---|
| `smoke` | `task_completion`, `answer_relevancy` | cheap first check |
| `core` | `task_completion`, `step_efficiency`, `correctness` | every agent task |
| `tools` | `core` + `tool_correctness`, `argument_correctness` | tool-use quality |
| `code` | `core` + `code_change_quality` | repo/code changes |
| `docs` | `core` + `faithfulness`, `contextual_relevancy` | document QA/grounding |
| `format` | `core` + `prompt_alignment` | strict formatting/instruction cases |
| `safety` | `bias`, `toxicity`, `pii_leakage` | safety-sensitive cases |
| `conversation` | `conversation_completeness`, `turn_relevancy`, `conversational_correctness` | multi-turn only |
| `full` | all metrics valid for the case's fields | broad audit, slower |

The default for a case without a profile is `core`. The first benchmark should use `core` for most cases, `tools` for tool-use cases, `docs` for document cases, and `code` for repo cases.

### 7.3 Custom `GEval`: correctness

This is the "does the overall output match the expected output" judge. It is deliberately semantic, not string equality.

```python
from deepeval.metrics import GEval
from deepeval.test_case import SingleTurnParams

GEval(
    name="Correctness",
    evaluation_params=[
        SingleTurnParams.INPUT,
        SingleTurnParams.ACTUAL_OUTPUT,
        SingleTurnParams.EXPECTED_OUTPUT,
    ],
    criteria=(
        "Compare the actual output with the expected output for the same input. "
        "Score 1.0 when the actual output agrees with every required fact, decision, "
        "or result and does not claim work that was not done. Score 0.5 when it is "
        "partially correct but misses a required fact or adds a minor unsupported "
        "claim. Score 0.0 when it contradicts the expected result, misses the core "
        "result, or claims completion when the evidence shows failure. Ignore "
        "wording, ordering, and formatting differences."
    ),
    threshold=case.threshold("correctness", 0.7),
    model=judge(),
)
```

For code cases, add a second `GEval` named `CodeChangeQuality` with `context` containing the workspace diff and command output:

```text
Score 1.0 if the diff fixes the stated problem, avoids unrelated edits, and the
project tests pass. Score 0.5 if it partially fixes the problem or includes
unrelated edits. Score 0.0 if tests fail, the wrong files changed, or the answer
claims a fix that the diff does not contain.
```

### 7.4 Field availability and validation

The runner must not let a metric fail at runtime because a field is missing. Validation rules:

- If `correctness` is enabled, `expected_output` is required.
- If `code_change_quality` is enabled, the harness supplies `context` from the
  behavioral workspace diff and `[[expect.commands]]` output; a case with no
  workspace diff is invalid for this metric.
- If `tool_correctness` is enabled, `expected_tools` (derived from `expect.tools` or an explicit list) is required.
- If `argument_correctness` is enabled and no tool calls occur, the metric scores 1.0 by DeepEval's behavior; the harness warns and the deterministic `expect.tools` check should catch missing calls.
- If `faithfulness` or `contextual_relevancy` is enabled, the case must provide static `retrieval_context` or set `grounding = "tool_outputs"` so the recorder can build it.
- In v1, JSON structure is checked deterministically with `expect.json_schema`
  (see the check suite); the `json_correctness` metric is phase 2 and needs a
  Pydantic model rather than a raw schema file.
- If `prompt_alignment` is enabled, the case must provide `prompt_instructions`.
- Multi-turn profiles cannot include single-turn metrics, and vice versa.

**Grounding source resolution** (`grounding`):

| Value | `retrieval_context` source |
|---|---|
| `static` (default when `retrieval_context` is present) | the case's `retrieval_context` array |
| `tool_outputs` | the recorded text outputs of `read_file`, `search_text`, `web_search`, and `fetch_url`, de-duplicated and clipped (e.g. 2,000 chars per item, max 20 items) |
| `none` (default) | no retrieval context; grounding metrics are invalid |

**Expected tools resolution:** `expected_tools` (explicit list) wins; otherwise the harness derives it from the names in `[[expect.tools]]` in declaration order. This keeps the manifest and `tool_correctness` consistent without duplicating names.

### 7.5 Threshold policy

Initial thresholds are hypotheses:

| Metric | Initial threshold |
|---|---|
| `task_completion` | 0.7 |
| `step_efficiency` | 0.6 |
| `correctness` | 0.7 |
| `tool_correctness` | 0.9 (or 1.0 with exact matching) |
| `argument_correctness` | 0.8 |
| `answer_relevancy` | 0.7 |
| `faithfulness` | 0.8 |
| `contextual_relevancy` | 0.7 |
| safety | 1.0 (strict) |

Do not lower a threshold just to make a failing case pass. If a metric repeatedly disagrees with human judgment, calibrate it against human annotations (Confident AI) rather than weakening the gate.

---

## 8. Dataset strategy

### 8.1 Two sources, one registry

1. **Curated artifact cases** (primary): 8–15 hand-designed cases covering repo edits, multi-document QA, tool selection, planning, and failure recovery. These are the cases where attaching artifacts matters.
2. **Generated cases** (breadth): use `deepeval generate` from the docs corpus to produce ~30–50 goldens, then import them as case directories.

The registry stays the source of truth. Generated cases are imported as normal `case.toml` files, marked `source = "generated"` and `enabled = false` until reviewed.

### 8.2 Synthetic generation commands

```bash
# Generate docs-based goldens.
deepeval generate \
  --method docs \
  --variation single-turn \
  --documents tests/evals/artifacts/product-docs \
  --output-dir tests/evals/.generated \
  --file-name .dataset.json

# Augment an existing small seed set.
deepeval generate \
  --method goldens \
  --variation single-turn \
  --goldens tests/evals/.dataset.json \
  --output-dir tests/evals/.generated \
  --file-name .dataset.augmented.json
```

Then:

```bash
python -m tests.evals.harness.cli import \
  --dataset tests/evals/.generated/.dataset.json \
  --bundle product-docs \
  --profile docs \
  --tag generated
```

The importer writes one directory per golden:

```text
cases/generated-0001/
  case.toml       # enabled = false, input/expected_output/context, bundle = product-docs
```

The user reviews the generated cases, fills in `expected_tools`/deterministic checks where useful, and enables them.

### 8.3 `.dataset.json` export

`evalctl export` writes `tests/evals/.dataset.json` from all enabled cases:

```json
[
  {
    "id": "my-code-case",
    "input": "...",
    "expected_output": "...",
    "expected_tools": [{"name": "read_file"}, {"name": "edit_file"}],
    "context": ["..."],
    "additional_metadata": {"tags": ["code"], "profile": "code", "artifact_sha256": "..."}
  }
]
```

This is for:
- sharing the benchmark without the artifacts,
- Confident AI dataset upload,
- `deepeval generate --method goldens` augmentation,
- diffing the benchmark over time.

The pytest suite does **not** load `.dataset.json`; it loads the registry so it has the artifacts. This deviation from the default template is intentional and documented for users.

### 8.4 Multi-turn (phase 2)

Two modes:

1. **Scripted multi-turn (deterministic regression):** a case declares `[[turns]]`; the runner calls `process_query` for each user turn on the same agent, then builds a `ConversationalTestCase` with `Turn(role="user"|"assistant", content=...)`, and runs only conversational metrics.
2. **Simulated multi-turn (exploratory):** a `ConversationalGolden` with `scenario`, `expected_outcome`, and an optional persona is passed to `ConversationSimulator` with a callback that wraps a fresh `EvalAgent`. The simulator generates user turns; the agent replies.

Both use `ConversationCompletenessMetric`, `TurnRelevancyMetric`, and a `ConversationalGEval` for product-specific criteria. Single-turn metrics are never used on these cases.

---

## 9. Add / remove / extend workflows

### Add a case

```bash
python -m tests.evals.harness.cli new repo-fix-002 --template code
# edit tests/evals/cases/repo-fix-002/case.toml
# drop the repo under tests/evals/cases/repo-fix-002/artifacts/repo/
python -m tests.evals.harness.cli validate repo-fix-002
python -m tests.evals.harness.cli run --case repo-fix-002
```

No harness code changes. No central index.

### Remove a case

```bash
rm -rf tests/evals/cases/repo-fix-002
# or set enabled = false in case.toml
```

### Attach a different artifact set

Drop files under the case's `artifacts/` and reference them:

```toml
[[workspace.artifacts]]
kind = "docs"
source = "artifacts/legal"
target = "docs/legal"
transform = "pdf_to_text"
```

Or reference a shared bundle:

```toml
[[workspace.artifacts]]
kind = "docs"
bundle = "product-docs"
target = "docs"
```

A case can attach any number of artifacts, of different kinds, to different targets.

### Add a metric

1. Implement a factory in `tests/evals/metrics.py`.
2. Register it in `METRIC_FACTORIES`.
3. Add it to a profile or enable it per case.

No test-file changes.

### Add an artifact transform

Implement it in `tests/evals/harness/workspace.py` and register it in `TRANSFORMS`. One place.

### Add a custom check

Add `checks.py` to the case directory and set `[checks] module = "checks.py"`. No harness changes.

---

## 10. Running the suite

### One case

```bash
deepeval test run tests/evals/test_agent_eval.py \
  -k my-case-001 \
  --identifier "calibrate-my-case-round-1"
```

### One profile or tag

`evalctl run` sets the case filter env vars and invokes DeepEval:

```bash
python -m tests.evals.harness.cli run --profile core
python -m tests.evals.harness.cli run --tag docs --identifier "docs-round-1"
python -m tests.evals.harness.cli run --case my-case-001
```

Equivalent raw command:

```bash
EVAL_PROFILE=core deepeval test run tests/evals/test_agent_eval.py \
  --identifier "core-round-1" \
  --ignore-errors \
  --skip-on-missing-params
```

### Full suite

```bash
deepeval test run tests/evals/test_agent_eval.py \
  --identifier "agent-benchmark-round-1" \
  --ignore-errors \
  --skip-on-missing-params
```

Start sequential for a local model. Use `--num-processes 5` only when the model endpoint and the sandbox can handle concurrent calls. The agent run itself is sequential per case in v1; parallel case execution is a phase 2 option (subprocess isolation).

### Serving model chain (Google AI Studio -> Ollama)

The model under test is selected by `tests/evals/harness/serving.py`, not by
application code. The default chain when a Google AI Studio key is available:

| order | target | role |
|---|---|---|
| 1 | `gemma-4-31b-it` | default serving model |
| 2 | `gemma-4-26b-a4b-it` | first fallback |
| 3 | `gemini-3.5-flash-lite` | safer fallback when Gemma is rate-limited/unavailable |
| 4 | `ollama/<AGENT_MODEL>` | final local safety net |

Google AI Studio's free tier is small (`~30` tokens/minute, `16k` context), so
the runner sets `Config.num_ctx` to `EVAL_SERVING_NUM_CTX` (default `16384`)
while the chain is active. The judge remains on local Ollama unless explicitly
changed.

**Architecture.**

- `ChatCompletionsLLM` is a harness-owned OpenAI-compatible client. It is used
  for Google targets and for optional local OpenAI-compatible targets.
- `FallbackLLM` implements the ordered `chat` / `chat_stream` interface the
  application already expects. `IntelligentAgent(cfg, llm=...)` receives it
  through `EvalAgent`; the application never imports the harness.
- `build_serving_llm(cfg)` returns `None` when no Google key is configured or an
  explicit non-Google `AGENT_PROVIDER` is set, so the application's normal
  `create_llm` path remains the default.

**Fallback policy.**

`FallbackLLM` switches only on retryable failures:

| reason | signals |
|---|---|
| `rate_limit` | `429`, `RESOURCE_EXHAUSTED`, quota, `TPM`, `RPM`, `too many requests` |
| `unavailable` | `500/502/503/504`, high demand, overloaded, connection/timeout |
| `unsupported_tools` | model does not support tools/function calling |
| `invalid_model` | model not found / not supported for `generateContent` |

Authentication and other client errors are fatal so a bad key or malformed
request is visible. Fallback is sticky for the rest of the case run: a target
that was rate-limited is not retried on every step. The last target's errors
propagate normally.

**Google compatibility shim.** The endpoint is OpenAI-compatible but stricter
than llama.cpp:

- Tool calls get stable ids and `type: "function"`.
- Tool-call arguments are serialized to JSON strings.
- Tool results are mapped to the matching `tool_call_id`; `tool_name` is removed.
- Gemini 3 function calls require the original `thought_signature` on later
  turns. Signatures are cached by `(tool name, canonical arguments)` because the
  application normalizes tool calls down to name+arguments. If a signature is
  missing (old transcript, resumed session), the exchange is replayed as plain
  text rather than failing the case. If Google still rejects a stale signature,
  the client retries once with every prior tool exchange flattened to text.
- Gemma's `<thought>...</thought>` blocks are stripped from the answer.

**Logging and reports.** `[eval-serving]` and `[eval-fallback]` lines are written
to the original stdout so they remain visible under pytest/DeepEval capture:

```text
[eval-serving] chain: google/gemma-4-31b-it -> ... -> ollama/nemotron-3.5-bolt:e4b-64k
[eval-fallback] rate_limit on google/gemma-4-26b-a4b-it: ... -> switching to google/gemini-3.5-flash-lite
```

`RunResult.model` / `provider` are the target that actually served the case.
`RunResult.model_chain` and `RunResult.fallbacks` are written to `result.json`,
`summary.json`, and the per-case `final.md`.

**Tests.** `tests/test_eval_harness.py` covers ordered switching, sticky
behavior, fatal auth errors, partial-stream safety, classification, the Google
message shim, thought stripping, missing-signature replay, chain construction,
and the no-key/local-only defaults.

### Judge model

The SUT model and the judge model are separate settings:

```bash
# Agent under test
export AGENT_PROVIDER=ollama
export AGENT_MODEL=your-agent-model

# Judge
export EVAL_JUDGE_PROVIDER=ollama
export EVAL_JUDGE_MODEL=your-judge-model
# or for a llama.cpp / OpenAI-compatible endpoint:
export EVAL_JUDGE_PROVIDER=local
export EVAL_JUDGE_BASE_URL=http://127.0.0.1:8080/v1
```

`tests/evals/harness/judge.py` maps these to `deepeval.models.OllamaModel` or `deepeval.models.LocalModel` (both verified available in 4.3.4). A stronger judge model is recommended even when the SUT is small.

### Raw pytest behavior

`tests/evals/conftest.py` skips the eval tests unless the DeepEval runner is active (`DEEPEVAL` env is set by `deepeval test run`). This keeps `pytest tests/` fast and avoids the `assert_test(golden=...)` "no active trace" error outside DeepEval.

---

## 11. Benchmarking across models

`evalctl run` records the model/provider/endpoint and writes a summary. To compare:

```bash
python -m tests.evals.harness.cli run --tag core --identifier "model-a"
AGENT_MODEL=model-b python -m tests.evals.harness.cli run --tag core --identifier "model-b"
python -m tests.evals.harness.cli compare .runs/<run-a> .runs/<run-b>
```

The comparison table shows pass rate, mean score per metric, mean steps, mean latency, and infra-error count. This is the core "benchmarking" view. Tag cases by difficulty (`easy`, `medium`, `hard`) to slice results.

Aggregate metrics:

- **pass rate:** cases where all metrics pass and all deterministic checks pass
- **mean score per metric:** useful even when thresholds fail
- **mean steps / mean seconds:** efficiency
- **tool error rate:** tool calls with `ok=false`
- **infra error rate:** model/connection failures, excluded from quality aggregates
- **flake rate:** across `--repeat N`, cases that pass sometimes

---

## 12. Isolation, safety, determinism

### Isolation

- Fresh temp workspace and fresh agent home per case.
- `os.chdir(workspace)` during the run, restored in `finally`.
- No session reuse across cases.
- Artifacts are copied (or symlinked) into the sandbox; the originals are never modified.
- Reports are written outside the workspace.

### Safety

- **Bash is unrestricted.** Only run trusted cases. For untrusted cases, set `bash = false` and `network = false`; denied tools are removed from the schema and handler map.
- **Network is opt-in.** `network = false` removes `web_search` and `fetch_url`. Cases that need the web set `network = true` and are tagged `network`.
- **Artifacts may contain secrets.** Keep secrets out of `tests/evals/artifacts/`; `.runs/` is gitignored.
- **Prompt injection is a test subject, not an accident.** Adversarial documents belong in `safety`-tagged cases.
- A Docker/`sandbox-exec` runner is a later phase for untrusted code; v1 is a trusted local benchmark.

### Determinism

- `temperature = 0.0` by default; per-case override if needed.
- Fixed `num_ctx`, fixed `max_steps`, timeouts.
- Fresh session per case; no history leakage.
- Record model name/version, provider, endpoint, DeepEval version, artifact hashes, git commit.
- `--repeat N` for flaky metrics; report pass@N and mean/std.
- Judge temperature 0 where supported.
- Treat any `Model error:` / `Internal error (` output as an infra failure, not a low-quality answer.

---

## 13. Implementation phases and acceptance criteria

### Phase 0 — decisions (this document)

- Confirm judge model/provider and endpoint.
- Confirm agent model/provider for the SUT.
- Confirm dataset mix and first artifact set.
- Confirm tracing and Confident AI.
- Confirm the first benchmark scope (repo only, docs only, or mixed).

### Phase 1 — harness core (smallest end-to-end slice)

- `case.py`: discovery, TOML loading, validation.
- `workspace.py`: copy artifacts, setup commands, snapshot/diff.
- `recorder.py`: `RecordingToolbox`, `RunRecorder`, `EvalAgent`.
- `runner.py`: `@observe` run, trace update, deterministic checks.
- `metrics.py`: `smoke`, `core`, `tools`, `code` profiles + `Correctness` GEval.
- `test_agent_eval.py`: parametrized single-turn suite.
- 3 example cases: no-artifact reasoning, repo fix, multi-doc QA.
- `conftest.py` raw-pytest skip.
- `.gitignore` for `.runs/`, `.cache/`.

**Acceptance:**

- `evalctl validate` passes for all enabled cases.
- `deepeval test run tests/evals/test_agent_eval.py -k <case>` runs against a real model and produces scores.
- The repo case fails when the bug is present and passes when fixed.
- The trace contains agent + tool spans; `StepEfficiency` and `ToolCorrectness` produce scores.
- Adding a fourth case requires only a new directory.
- Removing/disabling a case removes it from the run.
- The report contains transcript, tool calls, workspace diff, checks, and scores.

### Phase 2 — breadth and UX

- `html_to_text`, `pdf_to_text`, `csv_to_markdown`, `unpack`, `url` artifacts.
- Shared bundles and `evalctl new/import/export/report`.
- Docs/grounding profile with captured tool evidence.
- `.dataset.json` export and `deepeval generate` import.
- Summary/comparison reports.
- Custom `checks.py` support.

### Phase 3 — conversation and scale

- Multi-turn scripted and simulated suites.
- `ConversationSimulator` callback.
- Subprocess/parallel case execution.
- Optional Docker runner.
- Confident AI reports and human annotations.
- CI workflow.

---

## 14. Decisions (confirmed)

- **Judge model:** Local Ollama via `deepeval.models.OllamaModel`, temperature 0.
  Default judge: `gemma4:e4b-it-q4_K_M`; override with `EVAL_JUDGE_MODEL`.
- **Agent under test:** local Ollama, default `nemotron-3.5-bolt:e4b-64k`;
  override with `AGENT_MODEL` / `AGENT_PROVIDER` / `AGENT_BASE_URL`.
- **Dataset:** hybrid. 10–12 curated artifact cases plus ~30 generated docs
  cases; generated cases start disabled until reviewed.
- **Tracing:** yes. Root `@observe(type="agent")` and one
  `@observe(type="tool")` span per tool call.
- **Confident AI:** local-only for now. Reports stay under
  `tests/evals/.runs/`; Confident AI can be enabled later without changing cases.
- **First benchmark scope:** mixed `core` + one repo case + one docs case, to
  prove per-case artifacts end to end.
- **Rounds:** one calibration round, then five eval/improve rounds.

### Still open (non-blocking)

- Exact generated docs corpus for the ~30 synthetic cases.
- Whether to add a Docker runner for untrusted bash cases (phase 3).
- Whether to send results to Confident AI after the local suite is stable.

---

## Validation performed for this design

These checks were run before writing this document; they are throwaway spikes, not
application code.

1. **TOML schema parses with the stdlib.** The full manifest example was loaded
   with `tomllib`; arrays of tables for artifacts, setup, files, commands, and
   tools all parsed correctly.
2. **Trace-scoped `assert_test(golden=...)` works.** A local probe with a custom
   `BaseMetric` confirmed that `input`, `actual_output`, `expected_output`,
   `context`, `retrieval_context`, `tools_called`, and `expected_tools` all reach
   the metric inside `deepeval test run`.
3. **Tool spans work with `@observe(type="tool")`, not `next_tool_span`.** The
   first probe proved that `next_tool_span` only stages defaults for the next
   span; it attached the tool output to the parent. The corrected probe produced
   a root `agent` span with a child `tool` span named `read_file` and the correct
   final output. The design in §6.3 uses the corrected pattern.
4. **The raw-pytest gate is viable.** `deepeval test run` sets `DEEPEVAL=1`, so
   `tests/evals/conftest.py` can skip the eval subtree under a plain `pytest`
   run while still allowing `deepeval test run`.

Probe output (abridged):

```text
TOML OK
PROBE_OK {'actual_output': 'final text', 'expected_output': 'expected text',
          'tools_called': [ToolCall(name="read_file", ...)], ...}
TRACE_DICT {"name": "run_agent", "type": "agent", "output": "final text",
            "children": [{"name": "read_file", "type": "tool",
                          "input": {"path": "x"}, "output": "file body"}]}
DEEPEVAL_ENV '1'
```

---

## Appendix A — DeepEval 4.3.4 API findings (verified)

- `deepeval 4.3.4` is installed.
- `assert_test(test_case=None, metrics=None, golden=None, ...)` supports the trace-scoped path:
  `assert_test(golden=golden, metrics=[...])`.
- That path requires an active trace and a `deepeval test run` invocation; it raises
  `DeepEvalError` if no active trace exists.
- The trace-scoped path reads:
  - `input` from `golden.input`
  - `actual_output` from the trace output
  - `expected_output` from `current_trace.expected_output` with a fallback to
    `golden.expected_output` for metric execution
  - `context` and `retrieval_context` from the trace, with `Golden` fallbacks
  - `tools_called` / `expected_tools` from the trace, with a `Golden` fallback for
    expected tools
- `update_current_trace(...)` accepts `input`, `output`, `expected_output`, `context`,
  `retrieval_context`, `tools_called`, `expected_tools`, `name`, `tags`, and `metadata`.
- `@observe` accepts `type=` and `metrics=`. `@observe(type="tool")` creates a
  tool span; `update_current_span(...)` fills it in. `next_tool_span(...)` only
  stages defaults for the next span and does **not** create one.
- A local spike validated the trace shape: a root `@observe(type="agent")`
  span with a child `@observe(type="tool")` span, plus `expected_output`,
  `context`, `retrieval_context`, `tools_called`, and `expected_tools` reaching
  a trace-scoped metric through `assert_test(golden=...)`.
- `StepEfficiencyMetric` and `TaskCompletionMetric` require only
  `input` + `actual_output` at validation time, but `StepEfficiencyMetric` reads
  `test_case._trace_dict` and therefore needs a real trace with spans.
- `ToolCorrectnessMetric` requires `input`, `tools_called`, `expected_tools`.
- `ArgumentCorrectnessMetric` requires `input`, `tools_called`.
- `FaithfulnessMetric` requires `input`, `actual_output`, `retrieval_context`.
- `ContextualRelevancyMetric` requires `input`, `retrieval_context`.
- `Golden` supports `id`, `input`, `expected_output`, `context`, `retrieval_context`,
  `expected_tools`, `additional_metadata`, `name`, `tags`, etc.
- `OllamaModel` and `LocalModel` are available in `deepeval.models`.
- `ConversationalGolden`, `ConversationalTestCase`, `Turn`, and
  `ConversationSimulator` are available for phase 2.

## Appendix B — Agent integration points (code-derived)

| Hook | Location | Harness use |
|---|---|---|
| `IntelligentAgent.__init__` | `context_agent/agent.py` | build a fresh agent per case; inject temp `Config.home` |
| `IntelligentAgent.process_query` | `context_agent/agent.py` | run one user turn; returns final text |
| `IntelligentAgent._run_turn` | `context_agent/agent.py` | bounded step loop; detect truncation suffixes |
| `Toolbox.run` | `context_agent/tools/registry.py` | single point to record every tool call and emit tool spans |
| `TOOL_SPECS` | `context_agent/tools/specs.py` | names available for allow/deny policy |
| `ToolExecutionContext.resolve` | `context_agent/tools/context.py` | CWD-relative paths; chdir into the sandbox |
| `BashTool.run` | `context_agent/tools/bash.py` | unrestricted shell; trusted cases only |
| `SessionStore` | `context_agent/storage/session_store.py` | transcript/snapshot/spill for reports |
| `Config` | `context_agent/config.py` | temp home, temperature, step/timeout limits, provider |
| `process_query` error strings | `context_agent/agent.py` | classify infra failures vs quality failures |
