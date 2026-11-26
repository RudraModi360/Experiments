import { test, describe, it, beforeEach, afterEach } from 'node:test';
import * as assert from 'node:assert';
import * as fs from 'fs';
import * as path from 'path';
import { TOOLS, executeTool, detectLoop, runAgent } from './agent.js';

describe('Agent Tools & Logic', () => {
  const testDir = path.join(process.cwd(), 'test-sandbox');

  beforeEach(() => {
    if (!fs.existsSync(testDir)) {
      fs.mkdirSync(testDir, { recursive: true });
    }
  });

  afterEach(() => {
    if (fs.existsSync(testDir)) {
      fs.rmSync(testDir, { recursive: true, force: true });
    }
  });

  it('defines exactly 3 tools with correct names', () => {
    assert.strictEqual(TOOLS.length, 3);
    const names = TOOLS.map(t => t.name).sort();
    assert.deepStrictEqual(names, ['bash', 'read_file', 'write_file']);
  });

  it('executeTool write_file and read_file works correctly', async () => {
    const filePath = path.join(testDir, 'hello.txt');
    const writeResult = await executeTool('write_file', { path: filePath, content: 'Hello, world!' });
    assert.ok(writeResult.includes('Successfully wrote'));

    const readResult = await executeTool('read_file', { path: filePath });
    assert.strictEqual(readResult, 'Hello, world!');
  });

  it('executeTool bash works correctly', async () => {
    const bashResult = await executeTool('bash', { command: 'echo "test-bash-output"' });
    assert.ok(bashResult.includes('test-bash-output'));
  });

  it('executeTool handles errors gracefully', async () => {
    const readResult = await executeTool('read_file', { path: 'non-existent-file-12345.txt' });
    assert.ok(readResult.includes('Error'));

    const bashResult = await executeTool('bash', { command: 'exit 1' });
    // execSync throws on exit 1
    assert.ok(bashResult.includes('Error'));
  });

  it('detects infinite loops correctly', () => {
    const history1 = [
      { name: 'read_file', args: { path: 'a.txt' } },
      { name: 'read_file', args: { path: 'a.txt' } }
    ];
    assert.strictEqual(detectLoop(history1), true);

    const history2 = [
      { name: 'read_file', args: { path: 'a.txt' } },
      { name: 'read_file', args: { path: 'b.txt' } }
    ];
    assert.strictEqual(detectLoop(history2), false);

    const history3 = [
      { name: 'read_file', args: { path: 'a.txt' } },
      { name: 'write_file', args: { path: 'a.txt', content: 'x' } },
      { name: 'read_file', args: { path: 'a.txt' } }
    ];
    assert.strictEqual(detectLoop(history3), true);
  });

  it('runAgent respects maxSteps guard when LLM keeps calling tools', async () => {
    // Mock fetch to simulate an LLM that endlessly calls read_file
    const mockFetch = async () => {
      return {
        ok: true,
        json: async () => ({
          message: {
            content: 'I am reading a file.',
            tool_calls: [
              {
                function: {
                  name: 'read_file',
                  arguments: { path: 'package.json' }
                }
              }
            ]
          }
        })
      };
    };

    const result = await runAgent('Read package.json', {
      maxSteps: 3,
      fetchFn: mockFetch as any
    });

    assert.ok(result.includes('maximum step limit of 3'));
  });

  it('runAgent returns final text when LLM finishes without tool calls', async () => {
    const mockFetch = async () => {
      return {
        ok: true,
        json: async () => ({
          message: {
            content: 'Task completed successfully.',
            tool_calls: []
          }
        })
      };
    };

    const result = await runAgent('Do something', {
      fetchFn: mockFetch as any
    });

    assert.strictEqual(result, 'Task completed successfully.');
  });
});
