import shutil
import tempfile
import unittest
from pathlib import Path
from src.migrate import migrate
from src.api import get_user
from src.ratelimit import SlidingWindowLimiter

ROOT = Path(__file__).resolve().parents[1]


class MigrationAndRateLimitTests(unittest.TestCase):
    def test_idempotent_migration_and_v1_v2_contracts(self):
        with tempfile.TemporaryDirectory() as td:
            db = Path(td) / "app.db"
            shutil.copy2(ROOT / "data" / "app.db", db)
            migrate(db)
            migrate(db)  # must be idempotent

            u1 = get_user(db, 1, "v2")
            self.assertEqual((u1["first_name"], u1["last_name"]), ("Alice", "Johnson"))
            u2 = get_user(db, 2, "v2")
            self.assertEqual((u2["first_name"], u2["last_name"]), ("Madonna", ""))
            u3 = get_user(db, 3, "v2")
            self.assertEqual((u3["first_name"], u3["last_name"]), ("Dr.", "Priya Nair"))
            u6 = get_user(db, 6, "v2")
            self.assertEqual((u6["first_name"], u6["last_name"]), ("Mei", "Lin"))
            u8 = get_user(db, 8, "v2")
            self.assertEqual((u8["first_name"], u8["last_name"]), ("", ""))

            # Legacy v1 still intact
            v1 = get_user(db, 1, "v1")
            self.assertEqual(v1["full_name"], "Alice Johnson")

    def test_sliding_window_boundary_and_denied_not_counted(self):
        rl = SlidingWindowLimiter(max_requests=2, window_seconds=10.0)
        self.assertTrue(rl.allow("u1", 0.0))
        self.assertTrue(rl.allow("u1", 5.0))
        self.assertFalse(rl.allow("u1", 6.0))  # denied; must not extend window!
        self.assertTrue(rl.allow("u1", 10.0))  # t=0.0 expired at t=10.0


if __name__ == "__main__":
    unittest.main()
