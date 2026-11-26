import unittest
from app.store import add, all_items
class T(unittest.TestCase):
    def setUp(self):
        # reset
        import app.store as s; s._items.clear()
    def test_add_once(self):
        add({"id":1}); self.assertEqual(len(all_items()),1)
    def test_no_dup(self):
        add({"id":2}); add({"id":2}); self.assertEqual(len(all_items()),2)
