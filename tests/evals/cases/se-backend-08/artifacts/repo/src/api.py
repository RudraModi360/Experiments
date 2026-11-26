import sqlite3
from pathlib import Path


def get_user(db_path: Path, user_id: int, version: str = "v1") -> dict | None:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    if not row:
        return None
    if version == "v1":
        return {"id": row["id"], "email": row["email"], "full_name": row["full_name"] or ""}
    return {
        "id": row["id"],
        "email": row["email"],
        "first_name": row["first_name"] or "",
        "last_name": row["last_name"] or "",
    }
