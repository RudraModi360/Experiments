import unittest
from lru import LRUCache


class LRUTest(unittest.TestCase):
    def test_get_refreshes_recency(self):
        c = LRUCache(2)
        c.put(1, 1)
        c.put(2, 2)
        c.get(1)          # 1 becomes most-recent
        c.put(3, 3)       # should evict 2, not 1
        self.assertEqual(c.get(1), 1)
        self.assertEqual(c.get(2), -1)

    def test_eviction_order(self):
        c = LRUCache(2)
        c.put(1, 1)
        c.put(2, 2)
        c.put(3, 3)
        self.assertEqual(c.get(1), -1)
