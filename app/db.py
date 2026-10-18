import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone

SCHEMA = """
CREATE TABLE IF NOT EXISTS deployments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    commit_hash TEXT NOT NULL,
    environment TEXT NOT NULL,
    build_time TEXT NOT NULL,
    deployed_at TEXT NOT NULL
)
"""


def db_path() -> str:
    return os.getenv("DB_PATH", "./data/app.db")


@contextmanager
def _connect():
    path = db_path()
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)  # the CI smoke test runs with no /data folder
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute(SCHEMA)
        yield conn
        conn.commit()
    finally:
        conn.close()


def record_deployment(commit_hash, environment, build_time, deployed_at=None):
    deployed_at = deployed_at or datetime.now(timezone.utc).isoformat(timespec="seconds")
    with _connect() as conn:
        conn.execute(
            "INSERT INTO deployments (commit_hash, environment, build_time, deployed_at) "
            "VALUES (?, ?, ?, ?)",
            (commit_hash, environment, build_time, deployed_at),
        )


def get_history(limit=20):
    with _connect() as conn:
        rows = conn.execute(
            "SELECT commit_hash, environment, build_time, deployed_at FROM deployments "
            "ORDER BY deployed_at DESC, id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]