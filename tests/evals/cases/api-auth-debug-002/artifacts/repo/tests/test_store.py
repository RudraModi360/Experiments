import unittest
from app.store import Store
import tempfile, os


class StoreTest(unittest.TestCase):
    def test_add_and_list(self):
        with tempfile.TemporaryDirectory() as d:
            store = Store(os.path.join(d, "t.json"))
            store.add("a")
            self.assertEqual(len(store.all()), 1)
