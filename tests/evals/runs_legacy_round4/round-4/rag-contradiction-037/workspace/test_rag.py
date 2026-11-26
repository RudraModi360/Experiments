import unittest
import os
import tempfile
import shutil
from rag import SimpleBM25, load_docs, get_retriever, tokenize

class TestRAGPipeline(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory with test markdown files
        self.test_dir = tempfile.mkdtemp()
        
        # Write test doc 1
        with open(os.path.join(self.test_dir, "policy-a.md"), "w") as f:
            f.write("# Policy A\nEffective: 2025-01-01.\nAnnual plans get 14-day refund window.")
            
        # Write test doc 2
        with open(os.path.join(self.test_dir, "policy-b.md"), "w") as f:
            f.write("# Policy B\nEffective: 2026-03-01. Supersedes policy-a.md.\nAnnual plans get 30-day refund window.")
            
        # Write test doc 3
        with open(os.path.join(self.test_dir, "limits.md"), "w") as f:
            f.write("# Limits\nPro tier API rate limit is 1000 requests per minute.")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_tokenize(self):
        text = "Hello, World! Pro-tier: 1000 req/min."
        tokens = tokenize(text)
        self.assertIn("hello", tokens)
        self.assertIn("world", tokens)
        self.assertIn("pro", tokens)
        self.assertIn("tier", tokens)
        self.assertIn("1000", tokens)

    def test_load_docs(self):
        docs = load_docs(self.test_dir)
        self.assertGreaterEqual(len(docs), 3)
        sources = {d['source'] for d in docs}
        self.assertIn("policy-a.md", sources)
        self.assertIn("policy-b.md", sources)
        self.assertIn("limits.md", sources)

    def test_bm25_retrieval_refund(self):
        bm25 = get_retriever(self.test_dir)
        results = bm25.search("refund window annual plans", top_k=1)
        self.assertTrue(len(results) > 0)
        top_res = results[0]
        self.assertIn("refund window", top_res['text'].lower())
        self.assertIn("annual plans", top_res['text'].lower())

    def test_bm25_retrieval_rate_limit(self):
        bm25 = get_retriever(self.test_dir)
        results = bm25.search("Pro tier API rate limit", top_k=1)
        self.assertTrue(len(results) > 0)
        top_res = results[0]
        self.assertEqual(top_res['source'], "limits.md")
        self.assertIn("1000", top_res['text'])

    def test_bm25_ranking_relevance(self):
        bm25 = get_retriever(self.test_dir)
        # Search specifically for policy b keyword 30-day
        results = bm25.search("30-day", top_k=2)
        self.assertTrue(len(results) > 0)
        self.assertEqual(results[0]['source'], "policy-b.md")

if __name__ == "__main__":
    unittest.main()
