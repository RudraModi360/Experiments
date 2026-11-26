import json
import unittest
from pathlib import Path
from rag.retriever import PolicyRetriever

ROOT = Path(__file__).resolve().parents[1]


class RagEvalTests(unittest.TestCase):
    def setUp(self):
        self.retriever = PolicyRetriever(ROOT / "corpus")

    def test_recall_at_3(self):
        rows = [json.loads(l) for l in (ROOT / "eval" / "golden_qa.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
        hits = 0
        for r in rows:
            res = self.retriever.query(r["q"], category=r["category"], top_k=3)
            if any(c["doc_id"] == r["expected_doc"] and r["expected_clause"] in c["text"] for c in res):
                hits += 1
        recall = hits / len(rows)
        self.assertGreaterEqual(recall, 0.95, f"Recall@3 too low: {recall:.2f} ({hits}/{len(rows)})")

    def test_prompt_injections_stripped(self):
        forbidden = ["IGNORE PREVIOUS INSTRUCTIONS", "SECRET_KEY=PWNED", "SYSTEM OVERRIDE", "PROMPT_INJECTION"]
        for ch in self.retriever.chunks:
            upper = ch["text"].upper()
            for marker in forbidden:
                self.assertNotIn(marker, upper, f"Injection leaked in chunk from {ch['doc_id']}")


if __name__ == "__main__":
    unittest.main()
