import unittest
from app.auth import issue_token
from app.routes import list_tasks
from app.store import Store
import tempfile, os


class TasksTest(unittest.TestCase):
    def test_list_tasks_at_token_boundary(self):
        # Cascading failure: depends on verify_token accepting the boundary.
        with tempfile.TemporaryDirectory() as d:
            store = Store(os.path.join(d, "t.json"))
            store.add("write docs")
            token = issue_token("bob", ttl=50, now=500)  # exp == 550
            body, status = list_tasks(store, token, now=550)
            self.assertEqual(status, 200)
            self.assertEqual(body["user"], "bob")
