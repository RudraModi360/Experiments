import unittest
from intervals import merge_intervals


class IntervalsTest(unittest.TestCase):
    def test_overlap(self):
        self.assertEqual(merge_intervals([[1, 3], [2, 6], [8, 10]]), [[1, 6], [8, 10]])

    def test_touching(self):
        self.assertEqual(merge_intervals([[1, 2], [2, 3]]), [[1, 3]])

    def test_unsorted(self):
        self.assertEqual(merge_intervals([[8, 10], [1, 3], [2, 6]]), [[1, 6], [8, 10]])
