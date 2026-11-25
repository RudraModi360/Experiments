"""Tests for mini_agent.py."""

import unittest
import tempfile
import os
from pathlib import Path

from mini_agent import (
    safe_calc,
    ToolRegistry,
    MiniAgent,
    load_scenario_from_jsonl,
)


class TestMiniAgent(unittest.TestCase):

    def test_safe_calc_valid(self):
        self.assertEqual(safe_calc("2 + 3 * 4"), 14)
        self.assertEqual(safe_calc("(2 + 3) * 4"), 20)
        self.assertEqual(safe_calc("10 / 2"), 5.0)
        self.assertEqual(safe_calc("2 ** 3"), 8)
        self.assertEqual(safe_calc("-5 + 3"), -2)

    def test_safe_calc_invalid_and_injection(self):
        # Invalid syntax
        with self.assertRaises(ValueError):
            safe_calc("2 +")
        # Injection / Built-ins / functions should be rejected
        with self.assertRaises(ValueError):
            safe_calc("__import__('os').system('ls')")
        with self.assertRaises(ValueError):
            safe_calc("print('hello')")
        with self.assertRaises(ValueError):
            safe_calc("x + 1")

    def test_tool_registry_kv(self):
        registry = ToolRegistry()
        # Set
        res_set = registry.call("kv_set", {"key": "foo", "value": "bar"})
        self.assertTrue(res_set["success"])
        self.assertEqual(res_set["result"], "Stored foo = bar")

        # Get
        res_get = registry.call("kv_get", {"key": "foo"})
        self.assertTrue(res_get["success"])
        self.assertEqual(res_get["result"], "bar")

        # Get non-existent key
        res_missing = registry.call("kv_get", {"key": "baz"})
        self.assertFalse(res_missing["success"])

    def test_unknown_tool(self):
        registry = ToolRegistry()
        res = registry.call("nonexistent_tool", {})
        self.assertFalse(res["success"])
        self.assertIn("Unknown tool", res["error"])

    def test_rag_search(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            docs_path = Path(tmpdir) / "docs"
            docs_path.mkdir()
            
            # Create sample doc files
            (docs_path / "intro.txt").write_text("Welcome to the mini agent documentation. Python is great.", encoding="utf-8")
            (docs_path / "guide.md").write_text("# RAG Guide\nRetrieval-augmented generation allows searching files.", encoding="utf-8")

            registry = ToolRegistry()
            registry.docs_dir = docs_path

            res = registry.call("rag_search", {"query": "retrieval", "top_k": 2})
            self.assertTrue(res["success"])
            results = res["result"]
            self.assertGreater(len(results), 0)
            self.assertIn("guide.md", results[0]["file"])

    def test_agent_happy_scenario(self):
        scenario = [
            {"tool": "calc", "args": {"expr": "10 + 20"}},
            {"tool": "kv_set", "args": {"key": "sum", "value": 30}},
            {"action": "finish", "output": "Successfully computed sum"}
        ]
        agent = MiniAgent(max_steps=5, scenario=scenario)
        transcript = agent.run()
        self.assertEqual(len(transcript), 3)
        self.assertEqual(transcript[0]["status"], "executed")
        self.assertEqual(transcript[0]["result"]["result"], 30)
        self.assertEqual(transcript[2]["status"], "finished")

    def test_max_step_guard(self):
        # Scenario that never finishes and exceeds max_steps
        scenario = [
            {"tool": "calc", "args": {"expr": f"{i} + 1"}}
            for i in range(20)
        ]
        agent = MiniAgent(max_steps=3, scenario=scenario)
        transcript = agent.run()
        self.assertEqual(len(transcript), 3)

    def test_loop_detection_guard(self):
        # Scenario with 3 identical consecutive tool calls
        scenario = [
            {"tool": "calc", "args": {"expr": "2 + 2"}},
            {"tool": "calc", "args": {"expr": "2 + 2"}},
            {"tool": "calc", "args": {"expr": "2 + 2"}},
            {"tool": "calc", "args": {"expr": "2 + 2"}},
        ]
        agent = MiniAgent(max_steps=10, scenario=scenario)
        transcript = agent.run()
        # Should halt on the 3rd identical action
        self.assertEqual(len(transcript), 3)
        self.assertEqual(transcript[2]["status"], "halted_loop")
        self.assertIn("Loop detected", transcript[2]["result"]["error"])


if __name__ == "__main__":
    unittest.main()
