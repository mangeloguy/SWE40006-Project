import sqlite3
from contextlib import closing

import pytest
from fastapi.testclient import TestClient

from app import db
from app.main import app


@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    monkeypatch.setenv("DB_PATH", str(tmp_path / "test.db"))


def test_deployment_record_is_persisted():
    """After writing a deployment record, the same commit, environment and time are read back."""
    db.record_deployment(
        "a3f9c2e", "staging", "2026-10-18T10:00:00Z", deployed_at="2026-10-18T10:05:00+00:00"
    )

    assert db.get_history() == [
        {
            "commit_hash": "a3f9c2e",
            "environment": "staging",
            "build_time": "2026-10-18T10:00:00Z",
            "deployed_at": "2026-10-18T10:05:00+00:00",
        }
    ]


def test_deployment_history_is_ordered():
    """History is returned newest first, whatever order the rows were written in."""
    db.record_deployment("aaaaaaa", "staging", "t1", deployed_at="2026-10-18T09:00:00+00:00")
    db.record_deployment("ccccccc", "staging", "t3", deployed_at="2026-10-18T11:00:00+00:00")
    db.record_deployment("bbbbbbb", "production", "t2", deployed_at="2026-10-18T10:00:00+00:00")

    commits = [row["commit_hash"] for row in db.get_history()]

    assert commits == ["ccccccc", "bbbbbbb", "aaaaaaa"]


def test_db_path_env_var_controls_location(tmp_path, monkeypatch):
    """Changing DB_PATH writes the record to that file, creating missing folders."""
    custom = tmp_path / "nested" / "custom.db"
    monkeypatch.setenv("DB_PATH", str(custom))

    db.record_deployment("a3f9c2e", "dev", "local")

    assert custom.exists()
    with closing(sqlite3.connect(custom)) as conn:
        assert conn.execute("SELECT COUNT(*) FROM deployments").fetchone()[0] == 1


def test_app_startup_records_a_deployment(monkeypatch):
    """Starting the app writes one row built from the environment variables."""
    monkeypatch.setenv("GIT_COMMIT", "abc1234")
    monkeypatch.setenv("APP_ENV", "staging")
    monkeypatch.setenv("BUILD_TIME", "2026-10-18T10:00:00Z")

    with TestClient(app):
        pass

    latest = db.get_history()[0]
    assert latest["commit_hash"] == "abc1234"
    assert latest["environment"] == "staging"


def test_app_stays_up_when_deployment_record_fails(monkeypatch):
    """The app can still start even if a DB write fails, and /health remains up."""
    def boom(*args, **kwargs):
        raise RuntimeError("db down")

    monkeypatch.setattr(db, "record_deployment", boom)

    with TestClient(app) as client:
        resp = client.get("/health")

    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_dashboard_falls_back_to_empty_history_on_db_error(monkeypatch):
    """When a DB read fails, the homepage returns an empty history instead of a 500 error."""
    def boom(*args, **kwargs):
        raise RuntimeError("db down")

    monkeypatch.setattr(db, "get_history", boom)

    with TestClient(app) as client:
        resp = client.get("/")

    assert resp.status_code == 200
    assert "No deployments recorded yet" in resp.text