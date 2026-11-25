"""Mini Agent Implementation.

Features:
1. Tool Registry:
   - calc: Safe calculation without eval (using ast parsing and operator mapping).
   - kv_set / kv_get: Key-value store operations.
   - rag_search: Search over ./docs directory.
2. Agent Loop & Guards:
   - Driven by fake_model(step, history) or scenario.jsonl.
   - Max-step guard.
   - Loop detection (3 consecutive identical tool calls / actions).
3. Structured logging and transcript output.
"""

from __future__ import annotations

import ast
import json
import operator
import os
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union


# =====================================================================
# 1. Safe Calculator (No eval)
# =====================================================================

SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def safe_calc(expr: str) -> Union[int, float]:
    """Evaluate a mathematical expression safely using AST parsing.
    Supports basic arithmetic (+, -, *, /, //, %, **), unary +/- and numbers.
    Rejects functions, variables, attributes, or arbitrary code execution.
    """
    if not isinstance(expr, str) or not expr.strip():
        raise ValueError("Expression must be a non-empty string")

    try:
        node = ast.parse(expr.strip(), mode="eval")
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax in expression: {expr}") from e

    def _eval(node: ast.AST) -> Union[int, float]:
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant type: {type(node.value)}")
        elif isinstance(node, ast.Num):  # Python < 3.8 compatibility
            return node.n
        elif isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in SAFE_OPERATORS:
                raise ValueError(f"Unsupported operator: {op_type.__name__}")
            left = _eval(node.left)
            right = _eval(node.right)
            return SAFE_OPERATORS[op_type](left, right)
        elif isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in SAFE_OPERATORS:
                raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
            operand = _eval(node.operand)
            return SAFE_OPERATORS[op_type](operand)
        else:
            raise ValueError(f"Unsupported expression node: {type(node).__name__}")

    return _eval(node)


# =====================================================================
# 2. Tool Registry & Built-in Tools
# =====================================================================

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Callable[..., Any]] = {}
        self.kv_store: Dict[str, Any] = {}
        self.docs_dir = Path("./docs")

        # Register default tools
        self.register("calc", self.tool_calc)
        self.register("kv_set", self.tool_kv_set)
        self.register("kv_get", self.tool_kv_get)
        self.register("rag_search", self.tool_rag_search)

    def register(self, name: str, func: Callable[..., Any]) -> None:
        self._tools[name] = func

    def call(self, name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        if name not in self._tools:
            return {"error": f"Unknown tool: {name}", "success": False}
        try:
            result = self._tools[name](**(args or {}))
            return {"result": result, "success": True}
        except Exception as e:
            return {"error": str(e), "success": False}

    def tool_calc(self, expr: str) -> Union[int, float]:
        return safe_calc(expr)

    def tool_kv_set(self, key: str, value: Any) -> str:
        self.kv_store[key] = value
        return f"Stored {key} = {value}"

    def tool_kv_get(self, key: str) -> Any:
        if key not in self.kv_store:
            raise KeyError(f"Key not found: {key}")
        return self.kv_store[key]

    def tool_rag_search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Search over ./docs directory for query terms."""
        docs_path = self.docs_dir
        if not docs_path.exists() or not docs_path.is_dir():
            return []

        query_lower = query.lower()
        query_terms = query_lower.split()
        results = []

        for path in docs_path.rglob("*"):
            if path.is_file():
                try:
                    content = path.read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    continue

                content_lower = content.lower()
                score = 0
                # Simple keyword matching score
                if query_lower in content_lower:
                    score += 10
                for term in query_terms:
                    score += content_lower.count(term)

                if score > 0:
                    # Find snippet around first match
                    idx = content_lower.find(query_terms[0] if query_terms else query_lower)
                    if idx == -1:
                        idx = 0
                    start = max(0, idx - 100)
                    end = min(len(content), idx + 200)
                    snippet = content[start:end].strip()

                    results.append({
                        "file": str(path.relative_to(docs_path)),
                        "score": score,
                        "snippet": snippet
                    })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]


# =====================================================================
# 3. Agent Loop & Guards
# =====================================================================

def fake_model(step: int, history: List[Dict[str, Any]], scenario: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """Default fake model logic or scenario-driven model."""
    if scenario and step - 1 < len(scenario):
        return scenario[step - 1]
    
    # Default behavior if no scenario
    return {"action": "finish", "output": "Default completion"}


class MiniAgent:
    def __init__(self, registry: Optional[ToolRegistry] = None, max_steps: int = 10, scenario: Optional[List[Dict[str, Any]]] = None):
        self.registry = registry or ToolRegistry()
        self.max_steps = max_steps
        self.scenario = scenario
        self.history: List[Dict[str, Any]] = []

    def run(self) -> List[Dict[str, Any]]:
        """Run the agent loop with max-step guard and loop detection (3 repeats)."""
        transcript: List[Dict[str, Any]] = []
        recent_actions: List[str] = []

        for step in range(1, self.max_steps + 1):
            # Guard: Max steps
            if step > self.max_steps:
                break

            # Get action from model
            action = fake_model(step, self.history, self.scenario)
            
            # Check action type
            action_type = action.get("action") or action.get("tool")
            
            # Serialize action representation for loop detection
            action_key = json.dumps(action, sort_keys=True)
            
            # Guard: Loop detection (3 identical consecutive actions)
            recent_actions.append(action_key)
            if len(recent_actions) >= 3 and recent_actions[-1] == recent_actions[-2] == recent_actions[-3]:
                step_record = {
                    "step": step,
                    "action": action,
                    "result": {"error": "Loop detected: 3 identical consecutive actions", "success": False},
                    "status": "halted_loop"
                }
                transcript.append(step_record)
                self.history.append(step_record)
                break

            if action.get("action") == "finish":
                step_record = {
                    "step": step,
                    "action": action,
                    "result": action.get("output", "finished"),
                    "status": "finished"
                }
                transcript.append(step_record)
                self.history.append(step_record)
                break

            tool_name = action.get("tool")
            tool_args = action.get("args", {})

            if not tool_name:
                step_record = {
                    "step": step,
                    "action": action,
                    "result": {"error": "No tool specified", "success": False},
                    "status": "error"
                }
            else:
                tool_res = self.registry.call(tool_name, tool_args)
                step_record = {
                    "step": step,
                    "action": action,
                    "result": tool_res,
                    "status": "executed"
                }

            transcript.append(step_record)
            self.history.append(step_record)
        
        else:
            # If loop finished without break, check max steps exceeded
            if len(transcript) >= self.max_steps:
                # Add max step status if not already finished/halted
                pass

        return transcript


def load_scenario_from_jsonl(path: Union[str, Path]) -> List[Dict[str, Any]]:
    scenario = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                scenario.append(json.loads(line))
    return scenario
