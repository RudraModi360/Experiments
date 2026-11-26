import unittest
import os
import sys

# Ensure current directory is in sys.path
sys.path.insert(0, os.path.dirname(__file__))

from rag import SimpleBM25Retriever

class TestSimpleBM25Retriever(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.retriever = SimpleBM25Retriever(docs_dir="docs")

    def test_retriever_initialization(self):
        """Test that retriever loads chunks and builds index successfully."""
        self.assertGreater(len(self.retriever.chunks), 0)
        self.assertGreater(len(self.retriever.idf), 0)

    def test_search_refund_window(self):
        """Test search for annual plan refund window."""
        results = self.retriever.search("annual plan refund window", top_k=3)
        self.assertGreater(len(results), 0)
        top_chunk = results[0]["chunk"]
        # Should match billing policy docs
        self.assertIn("billing-policy", top_chunk["source"])
        self.assertIn("refund window", top_chunk["text"].lower())

    def test_search_rate_limits(self):
        """Test search for Pro API rate limit."""
        results = self.retriever.search("Pro API rate limit", top_k=3)
        self.assertGreater(len(results), 0)
        top_chunk = results[0]["chunk"]
        self.assertEqual(top_chunk["source"], "rate-limits.md")
        self.assertIn("Pro", top_chunk["text"])

    def test_search_tokenization(self):
        """Test tokenizer extracts alphanumeric words correctly."""
        tokens = self.retriever.tokenize("Hello, World! Pro Tier 1000 req/min.")
        self.assertIn("hello", tokens)
        self.assertIn("pro", tokens)
        self.assertIn("1000", tokens)

    def test_search_empty_or_nonsense_query(self):
        """Test search with query that has no matching terms."""
        results = self.retriever.search("zzzznonexistentqueryzzzz", top_k=2)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["score"], 0.0)

if __name__ == "__main__":
    unittest.main()
