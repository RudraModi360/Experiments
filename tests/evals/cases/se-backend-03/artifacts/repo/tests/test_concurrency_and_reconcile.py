import csv
import tempfile
import threading
import unittest
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from app.db import connect, init_db
from app.ledger import apply_refund_webhook, compute_total, create_charge

ROOT = Path(__file__).resolve().parents[1]


class LedgerConcurrencyAndReconcileTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Path(self.tmp.name) / "ledger.db"
        init_db(self.db)

    def tearDown(self):
        self.tmp.cleanup()

    def test_concurrent_idempotent_charges(self):
        results = []
        barrier = threading.Barrier(10)

        def worker():
            barrier.wait()
            res = create_charge(self.db, "idem-checkout-999", "19.95", "USD", "0.075")
            results.append(res["charge_id"])

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(len(set(results)), 1, f"Multiple charge IDs created: {results}")
        conn = connect(self.db)
        count = conn.execute("SELECT COUNT(*) FROM charges WHERE idempotency_key='idem-checkout-999'").fetchone()[0]
        conn.close()
        self.assertEqual(count, 1)

    def test_duplicate_refund_webhook_ignored(self):
        ch = create_charge(self.db, "idem-ref-1", "50.00", "USD", "0.10")
        r1 = apply_refund_webhook(self.db, "evt-dup-1", ch["charge_id"], "10.00")
        r2 = apply_refund_webhook(self.db, "evt-dup-1", ch["charge_id"], "10.00")
        self.assertTrue(r1)
        self.assertFalse(r2)
        conn = connect(self.db)
        count = conn.execute("SELECT COUNT(*) FROM refunds WHERE event_id='evt-dup-1'").fetchone()[0]
        conn.close()
        self.assertEqual(count, 1)

    def test_reconciliation_zero_drift(self):
        with (ROOT / "data" / "reconciliation_dump.csv").open("r", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        for r in rows:
            q = Decimal("1") if r["currency"] == "JPY" else Decimal("0.01")
            amt = Decimal(r["amount"]).quantize(q, rounding=ROUND_HALF_UP)
            expected_tax = (amt * Decimal(r["tax_rate"])).quantize(q, rounding=ROUND_HALF_UP)
            expected_total = amt + expected_tax
            _, tax, total = compute_total(r["amount"], r["currency"], r["tax_rate"])
            self.assertEqual(Decimal(tax), expected_tax, msg=f"Tax mismatch for {r}")
            self.assertEqual(Decimal(total), expected_total, msg=f"Total mismatch for {r}")


if __name__ == "__main__":
    unittest.main()
