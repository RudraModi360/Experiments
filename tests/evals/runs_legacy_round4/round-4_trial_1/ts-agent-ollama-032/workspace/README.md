# TypeScript Ollama Agent

A lightweight TypeScript autonomous agent running on a local Ollama model with three core tools (`read_file`, `write_file`, `bash`), a robust tool execution loop, max-step guard, and loop detection.

## Features

1. **Local Ollama Integration**: Communicates with Ollama (defaulting to `http://localhost:11434` and model `llama3` or `qwen2.5`) with structured tool-calling support.
2. **Exactly 3 Essential Tools**:
   - `read_file`: Read contents of any text file.
   - `write_file`: Create or overwrite files.
   - `bash`: Execute arbitrary bash commands safely on the host system.
3. **Safety & Loop Detection**:
   - **Max-Step Guard**: Prevents runaway execution by enforcing a strict step ceiling (default: 10 steps).
   - **Loop Detection**: Identifies repeated tool calls with identical arguments or cyclic tool sequences and halts execution to avoid infinite loops.
4. **Comprehensive Tests**: Built using Node.js native test runner (`node --test`).
5. **Zero Heavy Build Dependencies**: Written in modern TypeScript, run directly with `tsx` or compiled via `tsc`.

---

## Prerequisites

- [Node.js](https://nodejs.org/) (v18+ recommended)
- [Ollama](https://ollama.com/) running locally (`ollama serve`) with a tool-capable model pulled (e.g. `ollama pull llama3` or `ollama pull qwen2.5`).

---

## Installation

```bash
npm install
```

---

## Usage

### Running the Agent

You can run the agent CLI by passing a prompt as an argument:

```bash
npm start -- "List the files in the current directory and read package.json"
```

Or programmatically:

```typescript
import { runAgent } from './agent.ts';

const result = await runAgent("Check git status and report back");
console.log(result);
```

### Running Tests

Run the test suite using Node.js built-in test runner:

```bash
npm test
```

---

## Architecture & Implementation (`agent.ts`)

- **Tools Definition**: JSON schema definitions passed to Ollama so the model knows how to format tool arguments.
- **Tool Execution**: `executeTool` dispatches calls securely to file system operations or child process execution.
- **Loop Detector**: `detectLoop` maintains a sliding history of recent tool calls (name + arguments hash / sequence) to catch redundant loops.
- **Agent Loop**: Coordinates conversation history between user, assistant, and tool outputs until the model provides a final text response or hits safety guardrails.

## License

MIT
