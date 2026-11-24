import unittest
from app.auth import issue_token
from app.routes import list_tasks
class TasksTest(unittest.TestCase):
    def test_list_tasks_at_token_boundary(self):
        t = issue_token("alice", ttl=100, now=1000)
        status, _ = list_tasks(t, now=1100)
        self.assertEqual(status, 200)
