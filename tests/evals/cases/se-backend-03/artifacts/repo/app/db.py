import sqlite3
from pathlib import Path


def connect(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path), timeout=30.0, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: Path) -> None:
    conn = connect(db_path)
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS charges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idempotency_key TEXT NOT NULL,
            currency TEXT NOT NULL,
            subtotal TEXT NOT NULL,
            tax TEXT NOT NULL,
            total TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS refunds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id TEXT NOT NULL,
            charge_id INTEGER NOT NULL,
            amount TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()
