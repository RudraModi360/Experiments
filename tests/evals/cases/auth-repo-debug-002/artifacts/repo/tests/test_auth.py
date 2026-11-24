import unittest
from app.auth import issue_token, verify_token
class AuthTest(unittest.TestCase):
    def test_valid_token(self):
        t = issue_token("alice", ttl=100, now=1000)
        self.assertEqual(verify_token(t, now=1050), "alice")
    def test_expired_token_rejected(self):
        t = issue_token("alice", ttl=100, now=1000)
        self.assertIsNone(verify_token(t, now=2000))
    def test_token_valid_at_expiry_boundary(self):
        t = issue_token("alice", ttl=100, now=1000)
        self.assertEqual(verify_token(t, now=1100), "alice")
