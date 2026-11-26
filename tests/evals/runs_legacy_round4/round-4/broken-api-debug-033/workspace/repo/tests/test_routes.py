import unittest
from app.auth import issue_token
from app.routes import list_items
class T(unittest.TestCase):
    def test_ok(self):
        t=issue_token("alice",ttl=100,now=1000); self.assertEqual(list_items(t,now=1050)[0],200)
    def test_boundary(self):
        t=issue_token("alice",ttl=100,now=1000); self.assertEqual(list_items(t,now=1100)[0],200)
    def test_unauth(self):
        self.assertEqual(list_items(None)[0],401)
