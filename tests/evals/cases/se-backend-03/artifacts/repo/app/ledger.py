import time
from decimal import Decimal
from pathlib import Path
from app.db import connect


def compute_total(amount: str, currency: str, tax_rate: str) -> tuple[str, str, str]:
    # BUG: float arithmetic causes penny drift and ignores JPY 0-decimal rule
    amt = float(amount)
    tax = round(amt * float(tax_rate), 2)
    total = round(amt + tax, 2)
    return f"{amt:.2f}", f"{tax:.2f}", f"{total:.2f}"


def create_charge(db_path: Path, idempotency_key: str, amount: str, currency: str, tax_rate: str) -> dict:
    conn = connect(db_path)
    try:
        row = conn.execute(
            "SELECT id, total FROM charges WHERE idempotency_key = ?",
            (idempotency_key,),
        ).fetchone()
        if row:
            return {"charge_id": row["id"], "total": row["total"], "duplicate": True}
        # Simulate slight processing delay exposing the check-then-insert race
        time.sleep(0.01)
        sub, tax, total = compute_total(amount, currency, tax_rate)
        cur = conn.execute(
            "INSERT INTO charges (idempotency_key, currency, subtotal, tax, total) VALUES (?, ?, ?, ?, ?)",
            (idempotency_key, currency, sub, tax, total),
        )
        conn.commit()
        return {"charge_id": cur.lastrowid, "total": total, "duplicate": False}
    finally:
        conn.close()


def apply_refund_webhook(db_path: Path, event_id: str, charge_id: int, amount: str) -> bool:
    # BUG: no deduplication on event_id
    conn = connect(db_path)
    try:
        conn.execute(
            "INSERT INTO refunds (event_id, charge_id, amount) VALUES (?, ?, ?)",
            (event_id, charge_id, str(Decimal(amount))),
        )
        conn.commit()
        return True
    finally:
        conn.close()
