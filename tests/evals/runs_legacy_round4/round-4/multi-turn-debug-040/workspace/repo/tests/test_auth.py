import unittest
from app.auth import issue_token, verify_token
class T(unittest.TestCase):
    def test_boundary(self):
        t=issue_token("alice",ttl=100,now=1000)
        self.assertEqual(verify_token(t,now=1100),"alice")
