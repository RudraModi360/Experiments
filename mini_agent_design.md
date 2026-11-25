# Mini Agent Design & Implementation

Let's carefully design `mini_agent.py` to meet all user requirements precisely:

1. **Tool Registry**:
   - `calc`: Safe calculation *without* `eval()` (using Python `ast` parsing, `operator` mapping, allowing basic math operations `+`, `-`, `*`, `/`, `**`, unary `-`, numbers, parenthesized expressions, rejecting function calls, attributes, variables, etc.).
   - `kv_set` (or `kv.set` / `set`): Key-value set tool (stores in a shared KV dict/state).
   - `kv_get` (or `kv.get` / `get`): Key-value get tool (retrieves from KV store).
   - `rag_search` (or `rag.search` / `search` / `rag`): RAG search over `./docs` directory (reads files in `./docs`, searches for query terms or keyword matches / simple text search or BM25/cosine/TF-IDF scoring, returning matching snippets or document contents).
   - Unknown tool handling: Gracefully returns an error or tool output indicating unknown tool, without crashing.

2. **Agent Loop & `fake_model(step, history)`**:
   - Takes `step` (int) and `history` (list of previous steps/actions/results).
   - Returns JSON actions (or dictionary / JSON string representing action, e.g. `{"tool": "calc", "args": {"expr": "2 + 2"}}` or `{"action": "finish"}` or similar).
   - Can be driven by `scenario.jsonl` (e.g. happy path, max-step scenario, repeat loop scenario).

3. **Guards & Detection**:
   - Max-step guard (halts agent if max steps reached).
   - Loop detection (detects 3 identical consecutive actions/tool calls, halts with loop error/guard).

4. **Testing (`test_mini_agent.py`)**:
   - `unittest` test suite testing all guards (max-step, 3 repeats loop detection), unknown tool handling, calc safety (rejecting injections/builtins while computing math), rag search over `./docs`.

5. **Demo (`demo_transcript.jsonl` & `README.md`)**:
   - Generates `demo_transcript.jsonl` with `{step, action}` entries.
   - Writes a clear `README.md` explaining mini agent usage and design.
