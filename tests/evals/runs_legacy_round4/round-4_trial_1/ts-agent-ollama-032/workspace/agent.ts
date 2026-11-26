import * as fs from 'fs';
import * as path from 'path';
import { execSync } from 'child_process';

// ==========================================
// Types & Interfaces
// ==========================================

export interface Tool {
  name: 'read_file' | 'write_file' | 'bash';
  description: string;
  parameters: {
    type: 'object';
    properties: Record<string, { type: string; description: string }>;
    required: string[];
  };
}

export interface ToolCall {
  name: 'read_file' | 'write_file' | 'bash';
  arguments: Record<string, any>;
}

export interface ChatMessage {
  role: 'system' | 'user' | 'assistant' | 'tool';
  content: string;
  tool_calls?: ToolCall[];
  name?: string;
}

export interface AgentOptions {
  model?: string;
  ollamaUrl?: string;
  maxSteps?: number;
  systemPrompt?: string;
  fetchFn?: typeof fetch;
}

// ==========================================
// Tool Implementations
// ==========================================

export const TOOLS: Tool[] = [
  {
    name: 'read_file',
    description: 'Read the contents of a file at a given path.',
    parameters: {
      type: 'object',
      properties: {
        path: { type: 'string', description: 'The file path to read.' }
      },
      required: ['path']
    }
  },
  {
    name: 'write_file',
    description: 'Write content to a file at a given path (creates parent directories if needed).',
    parameters: {
      type: 'object',
      properties: {
        path: { type: 'string', description: 'The file path to write.' },
        content: { type: 'string', description: 'The content to write into the file.' }
      },
      required: ['path', 'content']
    }
  },
  {
    name: 'bash',
    description: 'Execute a bash command in the workspace and return stdout/stderr.',
    parameters: {
      type: 'object',
      properties: {
        command: { type: 'string', description: 'The shell command to execute.' }
      },
      required: ['command']
    }
  }
];

export async function executeTool(name: string, args: Record<string, any>): Promise<string> {
  try {
    if (name === 'read_file') {
      const filePath = args.path;
      if (!filePath) return 'Error: missing path argument';
      if (!fs.existsSync(filePath)) {
        return `Error: file not found: ${filePath}`;
      }
      const content = fs.readFileSync(filePath, 'utf8');
      return content;
    } else if (name === 'write_file') {
      const filePath = args.path;
      const content = args.content ?? '';
      if (!filePath) return 'Error: missing path argument';
      const dir = path.dirname(filePath);
      if (dir && dir !== '.' && !fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
      fs.writeFileSync(filePath, content, 'utf8');
      return `Successfully wrote to ${filePath}`;
    } else if (name === 'bash') {
      const command = args.command;
      if (!command) return 'Error: missing command argument';
      const output = execSync(command, { encoding: 'utf8', timeout: 30000 });
      return output;
    } else {
      return `Error: unknown tool ${name}`;
    }
  } catch (err: any) {
    return `Error executing tool ${name}: ${err.message || err}`;
  }
}

// ==========================================
// Loop Detection & Safety
// ==========================================

export function detectLoop(history: { name: string; args: Record<string, any> }[]): boolean {
  if (history.length < 3) return false;
  // Check for immediate repetition of 2 or 3 tool calls
  const len = history.length;
  const last = history[len - 1];
  const prev = history[len - 2];
  const prev2 = history[len - 3];

  // If last 2 calls are identical
  if (last.name === prev.name && JSON.stringify(last.args) === JSON.stringify(prev.args)) {
    return true;
  }

  // If last 3 calls cycle (A -> B -> A)
  if (len >= 3 && last.name === prev2.name && JSON.stringify(last.args) === JSON.stringify(prev2.args)) {
    return true;
  }

  return false;
}

// ==========================================
// Ollama LLM Client
// ==========================================

export async function callOllama(
  messages: ChatMessage[],
  tools: Tool[],
  options: { model: string; ollamaUrl: string; fetchFn?: typeof fetch }
): Promise<{ content: string; tool_calls?: ToolCall[] }> {
  const fetchImpl = options.fetchFn || globalThis.fetch;
  if (!fetchImpl) {
    throw new Error('No fetch implementation available');
  }

  const url = `${options.ollamaUrl}/api/chat`;

  // Format tools for Ollama / OpenAI tool calling convention
  const formattedTools = tools.map(t => ({
    type: 'function',
    function: {
      name: t.name,
      description: t.description,
      parameters: t.parameters
    }
  }));

  const payload = {
    model: options.model,
    messages: messages.map(m => {
      const msg: any = { role: m.role, content: m.content };
      if (m.tool_calls) {
        msg.tool_calls = m.tool_calls.map(tc => ({
          type: 'function',
          function: {
            name: tc.name,
            arguments: tc.arguments
          }
        }));
      }
      if (m.name) {
        msg.name = m.name;
      }
      return msg;
    }),
    tools: formattedTools,
    stream: false
  };

  const res = await fetchImpl(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  if (!res.ok) {
    const errText = await res.text();
    throw new Error(`Ollama API error (${res.status}): ${errText}`);
  }

  const data = await res.json();
  const message = data.message || {};
  
  let tool_calls: ToolCall[] | undefined = undefined;
  if (message.tool_calls && message.tool_calls.length > 0) {
    tool_calls = message.tool_calls.map((tc: any) => {
      let args = tc.function.arguments;
      if (typeof args === 'string') {
        try {
          args = JSON.parse(args);
        } catch {
          args = {};
        }
      }
      return {
        name: tc.function.name,
        arguments: args || {}
      };
    });
  }

  return {
    content: message.content || '',
    tool_calls
  };
}

// ==========================================
// Agent Runner
// ==========================================

export async function runAgent(prompt: string, options: AgentOptions = {}): Promise<string> {
  const model = options.model || process.env.OLLAMA_MODEL || 'llama3';
  const ollamaUrl = options.ollamaUrl || process.env.OLLAMA_URL || 'http://localhost:11434';
  const maxSteps = options.maxSteps || 10;
  const systemPrompt = options.systemPrompt || 
    'You are a helpful TypeScript assistant with access to 3 tools: read_file, write_file, and bash. Use them when appropriate to accomplish tasks.';

  const messages: ChatMessage[] = [
    { role: 'system', content: systemPrompt },
    { role: 'user', content: prompt }
  ];

  const toolHistory: { name: string; args: Record<string, any> }[] = [];
  let steps = 0;

  while (steps < maxSteps) {
    steps++;

    let assistantResponse;
    try {
      assistantResponse = await callOllama(messages, TOOLS, {
        model,
        ollamaUrl,
        fetchFn: options.fetchFn
      });
    } catch (err: any) {
      return `Agent error calling LLM: ${err.message || err}`;
    }

    messages.push({
      role: 'assistant',
      content: assistantResponse.content,
      tool_calls: assistantResponse.tool_calls
    });

    // If no tool calls, model has produced final response
    if (!assistantResponse.tool_calls || assistantResponse.tool_calls.length === 0) {
      return assistantResponse.content;
    }

    // Execute tool calls
    for (const tc of assistantResponse.tool_calls) {
      const toolName = tc.name;
      const toolArgs = tc.arguments || {};

      // Check loop detection
      toolHistory.push({ name: toolName, args: toolArgs });
      if (detectLoop(toolHistory)) {
        const loopWarning = `System Warning: Infinite loop detected for tool '${toolName}' with arguments ${JSON.stringify(toolArgs)}. Halting repeated tool call. Please try a different approach or conclude.`;
        messages.push({
          role: 'tool',
          name: toolName,
          content: loopWarning
        });
        continue;
      }

      // Execute tool
      const toolResult = await executeTool(toolName, toolArgs);
      messages.push({
        role: 'tool',
        name: toolName,
        content: toolResult
      });
    }
  }

  return `Agent stopped: reached maximum step limit of ${maxSteps}.`;
}
