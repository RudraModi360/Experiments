import * as fs from 'fs';
import * as path from 'path';
import { execSync } from 'child_process';

export interface Tool {
  name: string;
  description: string;
  parameters: {
    type: 'object';
    properties: Record<string, { type: string; description: string; [key: string]: any }>;
    required: string[];
  };
  execute: (args: any) => Promise<string> | string;
}

export interface Message {
  role: 'system' | 'user' | 'assistant' | 'tool';
  content: string;
  tool_calls?: Array<{
    id?: string;
    type?: string;
    function: {
      name: string;
      arguments: string | object;
    };
  }>;
  tool_call_id?: string;
  name?: string;
}

export interface AgentOptions {
  model?: string;
  ollamaUrl?: string;
  maxSteps?: number;
  systemPrompt?: string;
  verbose?: boolean;
}

export const tools: Tool[] = [
  {
    name: 'read_file',
    description: 'Read the contents of a text file. Supports offset and limit for pagination.',
    parameters: {
      type: 'object',
      properties: {
        path: { type: 'string', description: 'Path to the file to read' },
        offset: { type: 'number', description: 'Starting line number (1-based, optional)' },
        limit: { type: 'number', description: 'Maximum number of lines to read (optional)' },
      },
      required: ['path'],
    },
    execute: async (args: { path: string; offset?: number; limit?: number }) => {
      try {
        const resolvedPath = path.resolve(process.cwd(), args.path);
        if (!fs.existsSync(resolvedPath)) {
          return `Error: File not found: ${args.path}`;
        }
        const content = fs.readFileSync(resolvedPath, 'utf8');
        const lines = content.split('\n');
        const offset = args.offset && args.offset > 0 ? args.offset - 1 : 0;
        const limit = args.limit && args.limit > 0 ? args.limit : lines.length;
        const sliced = lines.slice(offset, offset + limit);
        return sliced.map((line, idx) => `${offset + idx + 1}: ${line}`).join('\n');
      } catch (err: any) {
        return `Error reading file: ${err.message}`;
      }
    },
  },
  {
    name: 'write_file',
    description: 'Create or overwrite a file with the given content.',
    parameters: {
      type: 'object',
      properties: {
        path: { type: 'string', description: 'Path to the file to write' },
        content: { type: 'string', description: 'Full content to write to the file' },
      },
      required: ['path', 'content'],
    },
    execute: async (args: { path: string; content: string }) => {
      try {
        const resolvedPath = path.resolve(process.cwd(), args.path);
        const dir = path.dirname(resolvedPath);
        if (!fs.existsSync(dir)) {
          fs.mkdirSync(dir, { recursive: true });
        }
        fs.writeFileSync(resolvedPath, args.content, 'utf8');
        return `Successfully wrote to ${args.path}`;
      } catch (err: any) {
        return `Error writing file: ${err.message}`;
      }
    },
  },
  {
    name: 'bash',
    description: 'Execute a bash command in the workspace root and return stdout/stderr.',
    parameters: {
      type: 'object',
      properties: {
        command: { type: 'string', description: 'Bash command to execute' },
      },
      required: ['command'],
    },
    execute: async (args: { command: string }) => {
      try {
        const output = execSync(args.command, {
          cwd: process.cwd(),
          encoding: 'utf8',
          timeout: 30000,
        });
        return output || '(Command executed with no output)';
      } catch (err: any) {
        let msg = err.message;
        if (err.stdout) msg += `\nStdout: ${err.stdout}`;
        if (err.stderr) msg += `\nStderr: ${err.stderr}`;
        return `Command failed: ${msg}`;
      }
    },
  },
];

export class Agent {
  model: string;
  ollamaUrl: string;
  maxSteps: number;
  systemPrompt: string;
  verbose: boolean;
  toolMap: Map<string, Tool>;

  constructor(options: AgentOptions = {}) {
    this.model = options.model || process.env.OLLAMA_MODEL || 'llama3.1';
    this.ollamaUrl = options.ollamaUrl || process.env.OLLAMA_URL || 'http://localhost:11434';
    this.maxSteps = options.maxSteps || 10;
    this.systemPrompt =
      options.systemPrompt ||
      'You are a helpful AI assistant with access to three tools: read_file, write_file, and bash. Use them when appropriate to accomplish tasks.';
    this.verbose = options.verbose ?? true;
    this.toolMap = new Map();
    for (const t of tools) {
      this.toolMap.set(t.name, t);
    }
  }

  // Format tools for Ollama API
  getOllamaTools() {
    return tools.map((t) => ({
      type: 'function',
      function: {
        name: t.name,
        description: t.description,
        parameters: t.parameters,
      },
    }));
  }

  // Call Ollama chat API
  async callOllama(messages: Message[]): Promise<Message> {
    const payload = {
      model: this.model,
      messages: messages,
      tools: this.getOllamaTools(),
      stream: false,
    };

    if (this.verbose) {
      console.log(`[Agent] Calling Ollama model ${this.model}...`);
    }

    const response = await fetch(`${this.ollamaUrl}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errText = await response.text();
      throw new Error(`Ollama API error (${response.status}): ${errText}`);
    }

    const data: any = await response.json();
    return data.message as Message;
  }

  // Detect loops in tool call history
  detectLoop(history: Message[]): boolean {
    // Look at recent assistant tool calls or tool call signatures
    const toolCalls: string[] = [];
    for (const msg of history) {
      if (msg.role === 'assistant' && msg.tool_calls) {
        for (const tc of msg.tool_calls) {
          const argsStr = typeof tc.function.arguments === 'string'
            ? tc.function.arguments
            : JSON.stringify(tc.function.arguments);
          toolCalls.push(`${tc.function.name}:${argsStr}`);
        }
      }
    }

    if (toolCalls.length < 3) return false;

    // Check for immediate repetition (e.g. same tool called with same args 3 times in a row)
    const last = toolCalls[toolCalls.length - 1];
    let streak = 0;
    for (let i = toolCalls.length - 1; i >= 0; i--) {
      if (toolCalls[i] === last) {
        streak++;
      } else {
        break;
      }
    }
    if (streak >= 3) return true;

    // Check for A-B-A-B pattern in last 4 calls
    if (toolCalls.length >= 4) {
      const c1 = toolCalls[toolCalls.length - 1];
      const c2 = toolCalls[toolCalls.length - 2];
      const c3 = toolCalls[toolCalls.length - 3];
      const c4 = toolCalls[toolCalls.length - 4];
      if (c1 === c3 && c2 === c4 && c1 !== c2) {
        return true;
      }
    }

    return false;
  }

  async run(prompt: string): Promise<string> {
    const messages: Message[] = [
      { role: 'system', content: this.systemPrompt },
      { role: 'user', content: prompt },
    ];

    let steps = 0;

    while (steps < this.maxSteps) {
      steps++;
      if (this.verbose) {
        console.log(`\n--- Step ${steps}/${this.maxSteps} ---`);
      }

      let assistantMsg: Message;
      try {
        assistantMsg = await this.callOllama(messages);
      } catch (err: any) {
        return `Error communicating with Ollama: ${err.message}. Is Ollama running?`;
      }

      messages.push(assistantMsg);

      if (this.verbose) {
        if (assistantMsg.content) {
          console.log(`[Assistant]: ${assistantMsg.content}`);
        }
        if (assistantMsg.tool_calls && assistantMsg.tool_calls.length > 0) {
          console.log(`[Assistant Tool Calls]:`, JSON.stringify(assistantMsg.tool_calls, null, 2));
        }
      }

      // If no tool calls, model responded with final answer
      if (!assistantMsg.tool_calls || assistantMsg.tool_calls.length === 0) {
        return assistantMsg.content || '';
      }

      // Check loop detection before executing tool calls
      if (this.detectLoop(messages)) {
        if (this.verbose) {
          console.log(`[Agent Warning] Loop detected! Stopping execution.`);
        }
        const loopMsg = 'System warning: Infinite or repetitive tool call loop detected. Please formulate a final answer or try a different approach.';
        messages.push({ role: 'user', content: loopMsg });
        // Give assistant one chance to respond without looping, or break
        try {
          const finalMsg = await this.callOllama(messages);
          return finalMsg.content || 'Loop detected and stopped.';
        } catch {
          return 'Loop detected and stopped.';
        }
      }

      // Execute tool calls
      for (const tc of assistantMsg.tool_calls) {
        const toolName = tc.function.name;
        let args = tc.function.arguments;
        if (typeof args === 'string') {
          try {
            args = JSON.parse(args);
          } catch {
            args = {};
          }
        }

        const tool = this.toolMap.get(toolName);
        let result: string;
        if (!tool) {
          result = `Error: Tool '${toolName}' not found.`;
        } else {
          if (this.verbose) {
            console.log(`[Executing Tool]: ${toolName} with args:`, JSON.stringify(args));
          }
          try {
            result = await tool.execute(args);
          } catch (err: any) {
            result = `Error executing tool ${toolName}: ${err.message}`;
          }
        }

        if (this.verbose) {
          console.log(`[Tool Result (${toolName})]:`, result.length > 500 ? result.slice(0, 500) + '...' : result);
        }

        messages.push({
          role: 'tool',
          name: toolName,
          content: result,
          tool_call_id: tc.id || 'call_' + Math.random().toString(36).substring(2, 9),
        });
      }
    }

    return `Agent reached max steps (${this.maxSteps}) without finishing.`;
  }
}

// CLI entry point if run directly
if (require.main === module) {
  const prompt = process.argv.slice(2).join(' ') || 'Hello! What can you do?';
  const agent = new Agent({ verbose: true });
  agent.run(prompt).then((res) => {
    console.log('\n=== Final Result ===\n', res);
  }).catch((err) => {
    console.error('Agent error:', err);
    process.exit(1);
  });
}
