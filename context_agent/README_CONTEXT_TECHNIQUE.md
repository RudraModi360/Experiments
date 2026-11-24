# Context Management Technique: Rolling Summarization with Multi-Stage Pipeline

## Overview

This is a **context management technique** that automatically keeps long-running agent conversations within token limits by maintaining a rolling summary of past interactions while preserving critical information. Instead of storing the entire conversation history, it uses a 5-stage pipeline to intelligently shrink, clear, and compress old messages as the conversation grows.

---

## Core Concept: The Budget Policy

The system operates like a budget manager with token-based limits:

```
┌─────────────────────────────────────────────────────────────────┐
│                    TOKEN BUDGET                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Model Window (e.g., 32768 tokens)                        │   │
│  │  ┌─────────────────────────────────────────────────┐    │   │
│  │  │  Usable Space = Window - Prediction Budget        │    │   │
│  │  │  (e.g., 32768 - 8192 = 24576 tokens)             │    │   │
│  │  │                                                  │    │   │
│  │  │  ┌─────────────────────────────────────────┐    │    │   │
│  │  │  │  Safety Margin (8% headroom)             │    │    │   │
│  │  │  │  → Actual Budget: ~22628 tokens          │    │    │   │
│  │  │  │                                         │    │    │   │
│  │  │  │  ┌─────────────────────────────────┐    │    │   │   │
│  │  │  │  │  Tools Token Cost (~1200)       │    │    │   │   │
│  │  │  │  │  ┌─────────────────────────┐   │    │   │   │   │
│  │  │  │  │  │  Usable Context Budget   │   │    │   │   │   │
│  │  │  │  │  │  → ~21428 tokens         │   │    │   │   │   │
│  │  │  │  │  │                          │    │    │   │   │   │
│  │  │  │  │  │  ┌───────────────────┐   │    │   │   │   │   │
│  │  │  │  │  │  │  Triggers:        │   │    │   │   │   │   │
│  │  │  │  │  │  │  • 75% → Start     │   │    │   │   │   │   │
│  │  │  │  │  │  │  • 62% → Clear Old  │   │    │   │   │   │   │
│  │  │  │  │  │  │  • Keep 35% Recent  │   │    │   │   │   │   │
│  │  │  │  │  │  └───────────────────┘   │    │   │   │   │   │
│  │  │  │  │  └─────────────────────────┘    │    │   │   │   │
│  │  │  │  └─────────────────────────────────┘    │    │   │   │
│  │  │  └─────────────────────────────────────────┘    │    │
│  │  └─────────────────────────────────────────────────┘    │
│  └─────────────────────────────────────────────────────────┘
└─────────────────────────────────────────────────────────────────┘
```

---

## The 5-Stage Maintain() Pipeline

When token usage exceeds the trigger threshold (75% of budget), the system runs through these stages:

### Stage 0: Repair (Always Runs)
**File:** `context/strategies/repair.py`

**Purpose:** Guarantee every tool call has exactly one result in the history.

**What it fixes:**
- Missing tool results (when a tool call wasn't answered)
- Empty assistant messages (messages with no content)
- Misaligned call/result pairs

**How it works:**
```python
# For each assistant message with tool_calls:
  collect all following tool messages until:
    - We have as many results as calls, OR
    - We hit a non-tool message
  If we're missing results → add stubbed "[no result: ...]" entries
```

**Output:** Returns a corrected history if changes were made, otherwise None.

---

### Stage 1: Freshness Check (Always Runs)
**File:** `context/strategies/freshness.py`

**Purpose:** Detect when files have changed outside the agent's control.

**What it does:**
- Compares file versions from `read_file` calls in history
- When a file's version changes, marks old read results as STALE
- Replaces stale content with: `[STALE: read_file of path lines X-Y (vOLD) - the file has since changed (now vNEW). Re-read it before relying on this.]`

**Why it matters:** Prevents the agent from acting on outdated information without knowing it.

---

### Stage 2: Deduplication (On Tool Call)
**File:** `context/strategies/dedupe.py`

**Purpose:** Remove duplicate and superseded tool outputs.

**What it detects:**
- **Exact duplicates:** Same tool, same args, same output → mark as "[duplicate: ...]"
- **Superseded reads:** If you read lines 1-100, then later read lines 50-150, the first read is superseded

**How it works:**
- Each tool call gets a SHA1 signature of (name + args + output)
- If signature matches an existing tool result → mark as duplicate
- For file reads: check if new read overlaps and extends beyond old read

---

### Stage 3: Clear Old Outputs (When Over Budget)
**File:** `context/strategies/clear.py`

**Purpose:** Shrink large tool outputs and call arguments to stubs.

**What it clears:**
1. **Large tool results** (>500 chars):
   - Saves full content to a spill file
   - Replaces with: `[CLEARED to save context: tool(args) -> N chars. Starts: '...'. Full copy: /path/to/spill/file.txt]`

2. **Long call arguments** (>600 chars):
   - Truncates to first 200 chars + "[N more chars omitted from history]"
   - Marks with `_meta["args_shrunk"] = True` (won't clear again)

**What it keeps:**
- Never clears the N most recent tool exchanges (`keep_recent_units`)
- Stops early if token count reaches target

**Spill files:** Full content is saved to `/sessions/spill/` with a tag and digest hash.

---

### Stage 4: Compaction (When Still Over Budget)
**File:** `context/strategies/compact.py`

**Purpose:** Fold the oldest whole conversation units into a rolling summary.

**What a "unit" is:** A user-assistant-tool sequence (one model turn)

**How it works:**
1. Groups history into message units (user, assistant, their tool calls)
2. Works from oldest to newest, accumulating token count
3. When adding more units would exceed the keep budget → STOP
4. Summarizes all units before the cut point into a single summary
5. Replaces old units with the summary in `state.summary`

**The summary format** (enforced by prompts):
```markdown
## Objective
What the user wants to achieve

## Constraints & preferences
User-specified constraints, preferences, error messages

## Progress
What has been accomplished

## Key findings
Important discoveries, decisions, exact values needed later

## Open items & next step
What remains to be done

## Dead ends
Brief note on approaches that didn't work (no repetition)
```

**LLM fallback:** If summarization fails or use_llm=False, uses a mechanical no-LLM digest that just head-tails each message.

---

### Stage 5: Emergency Truncation (If Still Over Limit)
**File:** `context/strategies/emergency.py`

**Purpose:** No-LLM fallback to guarantee the prompt never overflows.

**What it does:**
1. **Clear everything except 1 unit** (the most recent turn)
2. **Try compaction** 4 times with decreasing keep ratios (60%, 36%, 22%, 13%)
3. **If still over limit:** Truncate the largest message content
   - Splits long content: `[first 400 chars] ... [last 200 chars]`
   - Full content still in spill files

**Why it works:** Even if everything else fails, this guarantees the prompt fits.

---

## Key Configuration Values

From `config.py`:

| Config | Default | Meaning |
|--------|---------|---------|
| `safety_margin` | 0.92 | Keep 8% headroom for token counting errors |
| `trigger_ratio` | 0.75 | Start cleaning when we hit 75% of budget |
| `clear_target_ratio` | 0.62 | Step 3 aims to reduce to 62% |
| `keep_ratio` | 0.35 | Step 4 leaves ~35% recent history |
| `keep_recent_units` | 4 | Never clear the 4 most recent tool exchanges |
| `max_tool_chars` | 5000 | Max chars of one tool result kept in context |
| `max_unit_ratio` | 0.30 | All results of one model step share 30% of prompt |
| `max_summary_chars` | 4500 | Max size of the rolling summary |

---

## The View: What the Model Actually Sees

**File:** `context/view.py`

The `build()` method constructs the exact message list sent to the LLM:

```
[SYSTEM PROMPT]
  - Base prompt with instructions
  - Session memory (background context from earlier, if compacted)

[CONVERSATION HISTORY]
  - All messages after compaction
  - Cleaned (stripped of tool metadata)

[WORKING STATE]
  - Current request (user's latest message)
  - File paths being tracked
  - Auto-generated working state notes

[EPHEMERAL] (optional)
  - Temporary context passed per-turn
```

**Special handling:**
- If history starts with non-user → prepend user message with "[Earlier messages were compacted...]"
- Session memory is marked as background (user's newest message always takes priority)

---

## How It All Fits Together

```
┌──────────────────────────────────────────────────────────────────┐
│                        AGENT LOOP                                │
├──────────────────────────────────────────────────────────────────┤
│  1. User message arrives                                         │
│     ↓                                                            │
│  2. build_view() constructs the prompt                          │
│     ↓                                                            │
│  3. LLM generates response + tool calls                         │
│     ↓                                                            │
│  4. For each tool call:                                         │
│     - Execute tool                                              │
│     - add_tool_result() → triggers:                             │
│       • dedupe()                                                │
│       • freshness()                                             │
│       • clear() if over budget                                  │
│     ↓                                                            │
│  5. After all tools:                                            │
│     - maintain() → runs the 5-stage pipeline                    │
│       0. repair() → fix missing results                         │
│       1. freshness() → mark stale files                         │
│       2. (dedupe already ran per-call)                          │
│       3. clear() → shrink large outputs                         │
│       4. compact() → fold old units into summary                │
│       5. emergency() → truncate if still over limit             │
│     ↓                                                            │
│  6. Repeat with new user message                                │
└──────────────────────────────────────────────────────────────────┘
```

---

## Why This Technique is Effective

### 1. **Preserves Critical Information**
- Exact values (names, IDs, paths, URLs, commands) are explicitly kept in summaries
- Dead ends are recorded once so the agent doesn't repeat failed approaches
- Recent context is always preserved

### 2. **Handles External Changes**
- File freshness tracking detects when files change outside the agent
- Stale markers prevent acting on outdated data

### 3. **Graceful Degradation**
- Stage 3: Shrink large outputs (still has full content in spill files)
- Stage 4: Summarize old turns (LLM-based, preserves meaning)
- Stage 5: Mechanical truncation (guaranteed to fit, no LLM needed)

### 4. **No User Intervention Needed**
- Works transparently in the background
- User can say "continue" to resume after early stop
- Full context always available in spill files if needed

### 5. **Token Budget Optimization**
- Uses 35% of budget for recent history (where it matters most)
- 35% for rolling summary (preserves long-term context)
- 30% max per model turn (prevents one turn from dominating)

---

## Debugging & Monitoring

The system emits trace events for each stage:
- `repair: fixed_history` - how many corrections made
- `freshness: files_changed_outside_agent` - which files changed
- `clear: old_outputs_cleared` - how many messages cleared
- `compression: compacted` - tokens before/after
- `emergency: truncated_message` - which message was truncated

Enable with `cfg.verbose = True` in config.

---

## Limitations & Trade-offs

1. **Summary quality depends on LLM** - If summarization fails, falls back to mechanical digest
2. **Spill files grow** - Full content is saved externally; consider cleanup policies
3. **Session memory is one-way** - Compacted info doesn't flow back into active context
4. **Emergency truncation loses detail** - Last resort may cut important content

---

## When to Use This Technique

✅ **Long-running tasks** (code generation, multi-step research, data analysis)
✅ **Iterative conversations** (refining solutions, debugging)
✅ **Tasks requiring file operations** (reading/writing multiple files)
✅ **External context changes** (web research, monitoring file changes)

❌ **Short conversations** (<50 messages) - overhead not worth it
❌ **Tasks needing exact recall** (legal, medical) - consider full history
❌ **Token-count critical** - adds ~500-1000 tokens per compaction

---

## Files to Understand

| File | Purpose |
|------|---------|
| `context/manager.py` | Orchestrates the 5-stage pipeline |
| `context/strategies/*.py` | Individual strategy implementations |
| `context/view.py` | Builds the prompt the model sees |
| `context/summarizer.py` | Generates rolling summaries |
| `context/limits.py` | Computes token budgets |
| `config.py` | Runtime configuration |
| `agent.py` | Main agent loop that uses the context manager |

---

## Summary

This technique is a **proactive, multi-stage context management system** that:
- **Prevents** context overflow through budget-aware cleaning
- **Preserves** critical information in a rolling summary
- **Detects** external changes to maintain accuracy
- **Guarantees** operation even under extreme token pressure

It's essentially an automated "context janitor" that keeps the conversation clean while preserving what matters for future turns.
