import unittest
from heap import MinHeap
class HeapTest(unittest.TestCase):
    def test_order(self):
        h = MinHeap()
        for x in [3,1,2]: h.push(x)
        self.assertEqual(h.pop(), 1)
        self.assertEqual(h.pop(), 2)
        self.assertEqual(h.pop(), 3)
    def test_empty(self):
        h = MinHeap()
        self.assertIsNone(h.pop())
