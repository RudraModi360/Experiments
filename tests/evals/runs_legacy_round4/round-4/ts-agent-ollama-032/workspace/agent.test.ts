import { Agent, tools, Tool, Message } from './agent';
import * as fs from 'fs';
import * as path from 'path';

// Helper for assertions
function assert(condition: boolean, message: string) {
  if (!condition) {
    throw new Error(`Assertion failed: ${message}`);
  }
}

async function runTests() {
  console.log('=== Running Agent Tests ===\n');

  // Test 1: Tool Definitions
  console.log('Test 1: Verifying tools...');
  assert(tools.length === 3, 'Should have exactly 3 tools');
  const toolNames = tools.map((t) => t.name).sort();
  assert(
    JSON.stringify(toolNames) === JSON.stringify(['bash', 'read_file', 'write_file']),
    'Tools must be read_file, write_file, and bash'
  );
  console.log('✓ Tool definitions test passed.\n');

  // Test 2: Tool Execution - write_file & read_file
  console.log('Test 2: Testing write_file and read_file tools...');
  const testFilepath = 'test_sample.txt';
  const testContent = 'Hello, TypeScript Agent!\nLine 2 of test.';
  
  const writeTool = tools.find((t) => t.name === 'write_file')!;
  const readTool = tools.find((t) => t.name === 'read_file')!;

  const writeResult = await writeTool.execute({ path: testFilepath, content: testContent });
  assert(writeResult.includes('Successfully wrote'), 'write_file should succeed');

  const readResult = await readTool.execute({ path: testFilepath });
  assert(readResult.includes('Hello, TypeScript Agent!'), 'read_file should retrieve file content');
  assert(readResult.includes('2: Line 2 of test.'), 'read_file should include line numbers');

  // Test pagination
  const paginatedResult = await readTool.execute({ path: testFilepath, offset: 2, limit: 1 });
  assert(paginatedResult.includes('2: Line 2 of test.'), 'read_file pagination offset/limit should work');
  assert(!paginatedResult.includes('Hello'), 'paginated output should respect limit');

  // Cleanup test file
  if (fs.existsSync(testFilepath)) {
    fs.unlinkSync(testFilepath);
  }
  console.log('✓ write_file and read_file tests passed.\n');

  // Test 3: Tool Execution - bash
  console.log('Test 3: Testing bash tool...');
  const bashTool = tools.find((t) => t.name === 'bash')!;
  const bashResult = await bashTool.execute({ command: 'node -v' });
  assert(bashResult.startsWith('v'), 'bash tool should run node -v successfully');
  console.log(`✓ bash tool test passed (Node version: ${bashResult.trim()})\n`);

  // Test 4: Agent Loop Detection
  console.log('Test 4: Testing loop detection mechanism...');
  const agent = new Agent({ verbose: false });

  // Create a message history with repeating tool calls
  const loopHistory: Message[] = [
    { role: 'user', content: 'Do something looping' },
    {
      role: 'assistant',
      content: 'Calling tool',
      tool_calls: [
        {
          id: '1',
          function: { name: 'read_file', arguments: { path: 'nonexistent.txt' } },
        },
      ],
    },
    { role: 'tool', content: 'Error: not found', tool_call_id: '1' },
    {
      role: 'assistant',
      content: 'Calling tool again',
      tool_calls: [
        {
          id: '2',
          function: { name: 'read_file', arguments: { path: 'nonexistent.txt' } },
        },
      ],
    },
    { role: 'tool', content: 'Error: not found', tool_call_id: '2' },
    {
      role: 'assistant',
      content: 'Calling tool third time',
      tool_calls: [
        {
          id: '3',
          function: { name: 'read_file', arguments: { path: 'nonexistent.txt' } },
        },
      ],
    },
  ];

  const hasLoop = agent.detectLoop(loopHistory);
  assert(hasLoop === true, 'detectLoop should identify repeating tool calls (streak >= 3)');
  console.log('✓ Loop detection test passed.\n');

  // Test 5: Agent Max-Step Guard (Mocking callOllama to simulate infinite loop/steps)
  console.log('Test 5: Testing max-step guard...');
  const guardAgent = new Agent({ maxSteps: 2, verbose: false });
  // Mock callOllama to always return a tool call
  guardAgent.callOllama = async () => ({
    role: 'assistant',
    content: 'Still working...',
    tool_calls: [
      {
        id: 'call_mock',
        function: { name: 'bash', arguments: { command: 'echo step' } },
      },
    ],
  });

  const guardResult = await guardAgent.run('Run indefinitely');
  assert(
    guardResult.includes('max steps (2)'),
    `Result should indicate max steps reached, got: "${guardResult}"`
  );
  console.log('✓ Max-step guard test passed.\n');

  console.log('=== All Tests Passed Successfully! ===');
}

runTests().catch((err) => {
  console.error('Test failed with error:', err);
  process.exit(1);
});
