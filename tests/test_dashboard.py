import pytest
from fastapi.testclient import TestClient

from app.dashboard import render_dashboard
from app.main import app

INFO = {
    "status": "ok",
    "commit": "a3f9c2e",
    "environment": "staging",
    "build_time": "2026-10-18T10:00:00Z",
}


@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    monkeypatch.setenv("DB_PATH", str(tmp_path / "test.db"))


def test_render_shows_commit_environment_and_status():
    page = render_dashboard(INFO, [])
    assert "a3f9c2e" in page
    assert "staging" in page
    assert "Healthy" in page


def test_render_lists_history_rows():
    history = [
        {
            "commit_hash": "bbbbbbb",
            "environment": "production",
            "build_time": "t",
            "deployed_at": "2026-10-18T10:05:00+00:00",
        }
    ]
    page = render_dashboard(INFO, history)
    assert "bbbbbbb" in page
    assert "production" in page


def test_render_escapes_html():
    page = render_dashboard({**INFO, "commit": "<script>alert(1)</script>"}, [])
    assert "<script>alert" not in page
    assert "&lt;script&gt;" in page


def test_render_handles_empty_history():
    assert "No deployments recorded yet" in render_dashboard(INFO, [])


def test_dashboard_route_serves_page(monkeypatch):
    monkeypatch.setenv("GIT_COMMIT", "abc1234")
    monkeypatch.setenv("APP_ENV", "staging")
    with TestClient(app) as client:
        response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "abc1234" in response.text