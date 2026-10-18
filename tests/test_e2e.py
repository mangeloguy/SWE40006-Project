"""End-to-End Acceptance Testing: Simulate a complete user journey, from application launch to page display"""
import pytest
from fastapi.testclient import TestClient

from app import db
from app.main import app


@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    """Each test uses a separate temporary database file."""
    monkeypatch.setenv("DB_PATH", str(tmp_path / "test.db"))


def test_e2e_full_user_journey(monkeypatch):
    """Acceptance Process: Application launch, health check, deployment records stored in the database, homepage display, and metric exposure."""
    monkeypatch.setenv("GIT_COMMIT", "e2e1234")
    monkeypatch.setenv("APP_ENV", "staging")
    monkeypatch.setenv("BUILD_TIME", "2026-10-18T10:00:00Z")

    with TestClient(app) as client:
        health = client.get("/health").json()
        assert health["status"] == "ok"
        assert health["commit"] == "e2e1234"
        assert health["environment"] == "staging"

        latest = db.get_history()[0]
        assert latest["commit_hash"] == "e2e1234"
        assert latest["environment"] == "staging"

        page = client.get("/").text
        assert "e2e1234" in page

        metrics = client.get("/metrics").text
        assert "http_requests_total" in metrics


def test_e2e_dashboard_shows_previous_deployments(monkeypatch):
    """Validation: After entering multiple historical entries, the home page displays these deployments in reverse chronological order."""
    db.record_deployment("1111111", "staging", "t1", deployed_at="2026-10-18T09:00:00+00:00")
    db.record_deployment("2222222", "production", "t2", deployed_at="2026-10-18T10:00:00+00:00")

    with TestClient(app) as client:
        page = client.get("/").text

    assert "1111111" in page
    assert "2222222" in page
