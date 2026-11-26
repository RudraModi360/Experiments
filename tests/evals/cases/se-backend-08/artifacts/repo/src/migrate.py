import sqlite3
from pathlib import Path


def migrate(db_path: Path) -> None:
    # BUG: not idempotent, fails on mononyms/nulls, drops full_name breaking v1
    conn = sqlite3.connect(str(db_path))
    conn.execute("ALTER TABLE users ADD COLUMN first_name TEXT")
    conn.execute("ALTER TABLE users ADD COLUMN last_name TEXT")
    for uid, full_name in conn.execute("SELECT id, full_name FROM users").fetchall():
        first, last = full_name.split(" ")
        conn.execute("UPDATE users SET first_name=?, last_name=? WHERE id=?", (first, last, uid))
    conn.commit()
    conn.close()
