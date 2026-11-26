"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
const node_test_1 = require("node:test");
const assert = __importStar(require("node:assert"));
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const agent_js_1 = require("./agent.js");
(0, node_test_1.describe)('Agent Tools & Logic', () => {
    const testDir = path.join(process.cwd(), 'test-sandbox');
    (0, node_test_1.beforeEach)(() => {
        if (!fs.existsSync(testDir)) {
            fs.mkdirSync(testDir, { recursive: true });
        }
    });
    (0, node_test_1.afterEach)(() => {
        if (fs.existsSync(testDir)) {
            fs.rmSync(testDir, { recursive: true, force: true });
        }
    });
    (0, node_test_1.it)('defines exactly 3 tools with correct names', () => {
        assert.strictEqual(agent_js_1.TOOLS.length, 3);
        const names = agent_js_1.TOOLS.map(t => t.name).sort();
        assert.deepStrictEqual(names, ['bash', 'read_file', 'write_file']);
    });
    (0, node_test_1.it)('executeTool write_file and read_file works correctly', async () => {
        const filePath = path.join(testDir, 'hello.txt');
        const writeResult = await (0, agent_js_1.executeTool)('write_file', { path: filePath, content: 'Hello, world!' });
        assert.ok(writeResult.includes('Successfully wrote'));
        const readResult = await (0, agent_js_1.executeTool)('read_file', { path: filePath });
        assert.strictEqual(readResult, 'Hello, world!');
    });
    (0, node_test_1.it)('executeTool bash works correctly', async () => {
        const bashResult = await (0, agent_js_1.executeTool)('bash', { command: 'echo "test-bash-output"' });
        assert.ok(bashResult.includes('test-bash-output'));
    });
    (0, node_test_1.it)('executeTool handles errors gracefully', async () => {
        const readResult = await (0, agent_js_1.executeTool)('read_file', { path: 'non-existent-file-12345.txt' });
        assert.ok(readResult.includes('Error'));
        const bashResult = await (0, agent_js_1.executeTool)('bash', { command: 'exit 1' });
        // execSync throws on exit 1
        assert.ok(bashResult.includes('Error'));
    });
    (0, node_test_1.it)('detects infinite loops correctly', () => {
        const history1 = [
            { name: 'read_file', args: { path: 'a.txt' } },
            { name: 'read_file', args: { path: 'a.txt' } }
        ];
        assert.strictEqual((0, agent_js_1.detectLoop)(history1), true);
        const history2 = [
            { name: 'read_file', args: { path: 'a.txt' } },
            { name: 'read_file', args: { path: 'b.txt' } }
        ];
        assert.strictEqual((0, agent_js_1.detectLoop)(history2), false);
        const history3 = [
            { name: 'read_file', args: { path: 'a.txt' } },
            { name: 'write_file', args: { path: 'a.txt', content: 'x' } },
            { name: 'read_file', args: { path: 'a.txt' } }
        ];
        assert.strictEqual((0, agent_js_1.detectLoop)(history3), true);
    });
    (0, node_test_1.it)('runAgent respects maxSteps guard when LLM keeps calling tools', async () => {
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
        const result = await (0, agent_js_1.runAgent)('Read package.json', {
            maxSteps: 3,
            fetchFn: mockFetch
        });
        assert.ok(result.includes('maximum step limit of 3'));
    });
    (0, node_test_1.it)('runAgent returns final text when LLM finishes without tool calls', async () => {
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
        const result = await (0, agent_js_1.runAgent)('Do something', {
            fetchFn: mockFetch
        });
        assert.strictEqual(result, 'Task completed successfully.');
    });
});
