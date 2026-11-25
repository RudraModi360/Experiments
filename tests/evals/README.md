# Agent Evals — DeepEval-native suite

This suite evaluates the `context_agent` text-to-text, tool-using agent with
**DeepEval LLM metrics only**. The verdict for every case comes from a DeepEval
metric scored by an LLM judge; deterministic observations (workspace diff,
verification commands, custom checks) are collected as **evidence** for the
GEval judges and for the report — they never gate the result on their own.

Application code (`context_agent/`) is untouched. All instrumentation lives in
`tests/evals/harness/`.

## Mental model

A **case** is a directory under `cases/`:

```text
tests/evals/cases/<case-id>/
  case.toml          # turns/input, expected output/outcome, metrics, artifacts
  artifacts/         # repo/docs/files attached to a fresh sandbox
  checks.py          # optional deterministic EVIDENCE (not a gate)
  expected/          # optional schema files
```

Discovery is automatic: adding a case = adding a directory. There are two
suites:

| Suite | File | Case shape | Metrics |
|---|---|---|---|
| single-turn | `test_agent_eval.py` | `input` | `TaskCompletion`, `StepEfficiency`, `Correctness` GEval, tool/grounding/quality metrics |
| multi-turn | `test_agent_conversation.py` | `[[turns]]` on one session | `ConversationCompleteness`, `TurnRelevancy`, `ConversationalGEval` |

Never mix single-turn and multi-turn metrics: the suites are separate.

## Quick start

```bash
# Install everything (uzu + deepeval) — deepeval is a uv dev dependency
uv sync

# 1. Judge env (Google key enables the judge chain; no key -> Ollama judge only)
export OLLAMA_HOST=http://localhost:11434  # optional

# 2. SUT is the local uzu Qwen model by default (32k context)
#    Override with AGENT_MODEL / AGENT_PROVIDER / AGENT_BASE_URL / AGENT_NUM_CTX

# 3. Regenerate all artifacts (deterministic), then validate
uv run python tests/evals/artifacts/generate_fixtures.py
uv run python -m tests.evals.harness.cli validate

# 4. Run everything (both suites)
uv run python -m tests.evals.harness.cli run --run-id round-1

# One case / one suite / one profile
uv run python -m tests.evals.harness.cli run --case cli-greenfield-001
uv run python -m tests.evals.harness.cli run --suite conversation
uv run python -m tests.evals.harness.cli run --tag stress --identifier stress-round-1

# Inspect a report
uv run python -m tests.evals.harness.cli report
uv run python -m tests.evals.harness.cli report --case nginx-log-forensics-004
```

### Gemini via Google AI Studio (faster than the local SUT)

`GEMINI_API_KEY` is loaded from the repo `.env` automatically (shell variables
still win). To run one case with Gemini 3.5 Flash Lite as the SUT and the judge,
with no local Ollama fallback:

```bash
uv run python -m tests.evals.harness.cli run \
  --case weather-cli-011 \
  --serving-chain google:gemini-3.5-flash-lite \
  --no-final-ollama \
  --judge-provider google \
  --judge-model gemini-3.5-flash-lite \
  --run-id gemini-smoke
```

- Drop `--no-final-ollama` to keep `ollama:nemotron-3.5-bolt:e4b-64k` as a
  rate-limit/unavailable fallback.
- Drop `--judge-provider google --judge-model ...` to keep the default local
  Ollama judge.
- `--serving-chain` now enables the served SUT automatically; you no longer
  need to export `EVAL_SERVING_DISABLE=0`.
- Transient Google errors (503 "overloaded", timeouts) are retried on the same
  target before falling back: `EVAL_SERVING_RETRIES` (default `2`) and
  `EVAL_SERVING_RETRY_DELAY` seconds (default `2`, doubled per retry). Set
  `EVAL_SERVING_RETRIES=0` to disable.

Plain `pytest` skips these tests; always use `deepeval test run` (or `evalctl run`).
The harness CLI launches `.venv/bin/deepeval` from the active uv environment so
the eval subprocess and the SUT share one interpreter (Python 3.12 with uzu).
Running with system `python3` is not supported: it has deepeval but not uzu.

## Live progress

While a suite is running, the harness keeps one `[eval]` line pinned to the
terminal (the same idea as the CLI's live `[stats]` line):

```text
[eval] single 3/10 weather-cli-011 | code | agent | 01:42 | step 7 | 14 tools | last bash
```

It shows the case position, id, profile, phase (`workspace`, `agent`, `checks`,
`judging`, `report`), elapsed time, steps and tool calls. The line is written
straight to the terminal because pytest captures normal stdout. Each case also
prints static start and finish lines:

```text
[eval] single 3/10 weather-cli-011 | profile=code | starting
[eval] single 3/10 weather-cli-011 | ok | 128.4s | 7 steps | 14 tools | qwen3.5-9b
```

On a non-interactive terminal (CI, redirected output) only the static lines are
emitted, so logs still record every case. Disable the pinned line with
`EVAL_LIVE_PROGRESS=0`.

## Models

| Role | Default | Config |
|---|---|---|
| SUT | `trymirai/Qwen3.5-9B-M` via uzu (`AGENT_PROVIDER=uzu`, 32k ctx) | `AGENT_MODEL`, `AGENT_PROVIDER`, `AGENT_BASE_URL`, `AGENT_NUM_CTX` |
| SUT (served) | off by default; optional Google AI Studio chain | `EVAL_SERVING_CHAIN=google:gemini-3.5-flash-lite`, `EVAL_SERVING_DISABLE=0` |
| Judge | Ollama `nemotron-3.5-bolt:e4b-64k` | `EVAL_JUDGE_CHAIN`, or `EVAL_JUDGE_PROVIDER=ollama\|local\|google` |
| Environment | uv (Python 3.12); `uzu` runtime dep, `deepeval==4.3.4` dev dep | `uv sync`, `uv run ...` |

Judge fallback is sticky per case: a rate-limited target is not retried within
the same case. The final Ollama fallback saves an individual case when every
Google target fails. Authentication errors are fatal, not silently hidden.
The SUT's own Google serving chain is **disabled by default**
(`EVAL_SERVING_DISABLE=1`). Pass `--serving-chain google:<model>` (or set
`EVAL_SERVING_DISABLE=0`) to serve the SUT from Google AI Studio instead.

## The 12 cases

Single-turn (10):

| id | area | type | stress axis |
|---|---|---|---|
| `cli-greenfield-001` | CLI/stats | independent | baseline build+test+fix loop |
| `api-auth-debug-002` | backend | broken repo | cascading failure, minimal-diff |
| `frontend-state-debug-003` | frontend | broken repo | multi-file coherence, dedupe/superseded reads |
| `nginx-log-forensics-004` | devops | big log | 2.9MB log → spill + exact-number recall |
| `docker-greenfield-005` | docker | independent | cross-file exact-value consistency |
| `mini-agent-build-006` | agentic AI | independent | tool loop + guards + transcript |
| `rag-corpus-qa-007` | RAG/docs | build over corpus | read-all compaction + contradiction resolution |
| `dsa-modules-debug-008` | DSA | broken repo | algorithmic precision + complexity |
| `fullstack-spec-chaos-009` | full-stack | long spec | ~51k-char user spill + STALE/freshness |
| `docs-synthesis-injection-010` | docs/safety | docs+schema | injection resistance + strict JSON |

Multi-turn (2):

| id | area | shape |
|---|---|---|
| `conv-debug-refine-001` | iterative debugging | fix then extend on one session |
| `conv-doc-followup-002` | doc QA | changed-constraint follow-up, grounding across turns |

## Metrics

Profiles: `smoke`, `core`, `tools`, `code`, `docs`, `format`, `safety`,
`conversation`, `full`. They are defined in `metrics.py`; `use` adds and
`disable` removes metrics per case. Task-specific GEval judges:
`code_change_quality`, `instruction_hierarchy`, `cross_file_consistency`.

Thresholds are hypotheses, not knobs to weaken for a failing model. Treat
`Model error:` / `Internal error (` / timeouts as **infra failures**, not
quality scores.

## Reports

Every case writes to `tests/evals/.runs/<run-id>/<case-id>/`: workspace diff,
tool calls, transcript, deterministic evidence, metric scores, and the final
answer. `summary.json` / `summary.md` at the run root are the benchmark
artifact. No Confident AI upload by default.

## Clean / reset to untouched state

Agent runs execute in a **temporary sandbox** copied from case artifacts; they
do **not** modify `tests/evals/cases/**` source fixtures. What *does* get
written is run output: `.runs/` (reports, diffs, transcripts, and any preserved
failure workspace), `.deepeval/` traces/cache, `.pytest_cache`, and eval
caches. To reset:

```bash
# Remove all runs, traces, caches (keeps case definitions + fixtures)
uv run python -m tests.evals.harness.cli clean

# Remove only one run
uv run python -m tests.evals.harness.cli clean --run-id round-1
```

After `clean`, case fixtures are untouched and you can rerun from ground zero.

## Notes

- **Bash is unrestricted.** Sandboxes are workspaces, not security boundaries.
  Only run trusted cases. Network tools are removed unless `network = true`.
- **Deterministic `checks.py`** feeds evidence to the judge (e.g. compaction
  telemetry in case 004/007/009); it does not decide pass/fail.
- **DeepEval pytest plugin isolation:** the harness sets
  `PYTEST_ADDOPTS=-p no:deepeval` for sandbox subprocesses so a case's own
  `python -m unittest` / `node --test` runs are not contaminated.
- Full design history is in `DESIGN.md` (the harness structure remains valid;
  the verdict model and case registry are described here).
