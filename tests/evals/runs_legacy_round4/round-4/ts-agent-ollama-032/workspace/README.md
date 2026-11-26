# TypeScript Ollama Agent (`agent.ts`)

A lightweight, robust TypeScript autonomous agent that interacts with a local Ollama model using exactly 3 core system tools (`read_file`, `write_file`, and `bash`). 

Features include strict tool definitions, robust safety guardrails (max-step enforcement and automated loop detection), comprehensive unit/integration tests, and interactive CLI usage.

---

## Architecture & Features

1. **Local Ollama Integration**: Communicates via standard Ollama chat API (`/api/chat`) with JSON-formatted function/tool calling.
2. **Exactly 3 Core Tools**:
   - `read_file`: Reads text files with line numbers and optional pagination (`offset`, `limit`).
   - `write_file`: Creates or overwrites files on disk with confirmation feedback.
   - `bash`: Executes shell commands safely with stdout/stderr capture and timeout protection.
3. **Safety Guardrails**:
   - **Max-Step Guard**: Enforces an upper limit on agent execution steps (`maxSteps`, default: 15) to prevent runaway processes.
   - **Loop Detection**: Monitors history for repeating tool call signatures (`toolName + JSON.stringify(args)`). If a tool call repeats 3 times consecutively, the agent halts and injects a warning prompt into the conversation to break out of infinite loops.
4. **Interactive CLI & Programmatic API**: Can be run directly from the command line or imported into TypeScript/JavaScript applications.

---

## Installation & Setup

1. **Prerequisites**:
   - Node.js (v18+ recommended, tested on v24.21.0)
   - [Ollama](https://ollama.com/) running locally (`http://localhost:11434`) with a tool-capable model (e.g. `llama3`, `mistral`, or `qwen2.5`).

2. **Install Dependencies**:
   ```bash
   npm install
   ```

---

## Running the Agent

### CLI Mode
You can invoke the agent via `npm start` or directly via `npx ts-node`:

```bash
# Run with a prompt
npm start "List files in the current directory and read package.json"
```

Or configure environment variables:
- `OLLAMA_MODEL`: Model name (default: `llama3`)
- `OLLAMA_HOST`: Ollama server URL (default: `http://localhost:11434`)
- `AGENT_MAX_STEPS`: Max execution steps (default: `15`)

```bash
OLLAMA_MODEL=llama3 npm start "Check git status"
```

### Programmatic Usage

```typescript
import { Agent } from './agent';

async function main() {
  const agent = new Agent({
    model: 'llama3',
    maxSteps: 10,
    verbose: true,
  });

  const response = await agent.run('Create a greeting.txt file and write "Hello from agent!" into it.');
  console.log('Agent Response:', response);
}

main();
```

---

## Running Tests

The test suite (`agent.test.ts`) verifies:
- Tool definition correctness (exactly 3 tools).
- File reading (with pagination) and writing.
- Bash command execution.
- Loop detection algorithm on repeating tool calls.
- Max-step guard enforcement.

Run the tests with:
```bash
npm test
```

---

## Project Files

- **`agent.ts`**: Core agent implementation, tool definitions, Ollama API client loop, max-step guard, loop detector, and CLI runner.
- **`agent.test.ts`**: Comprehensive test script covering tools, loop detection, and guardrails.
- **`package.json`**: Project configuration with build, start, and test scripts.
- **`tsconfig.json`**: TypeScript compiler options.
