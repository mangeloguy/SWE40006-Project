
def test_health_returns_ok(client):
    """GET /health 返回 200，且 status 字段为 ok。"""
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_health_defaults_when_env_unset(client, monkeypatch):
    """If the relevant environment variables are not set, each field reverts to its default value"""
    monkeypatch.delenv("GIT_COMMIT", raising=False)
    monkeypatch.delenv("APP_ENV", raising=False)
    monkeypatch.delenv("BUILD_TIME", raising=False)

    body = client.get("/health").json()
    assert body["commit"] == "unknown"
    assert body["environment"] == "dev"
    assert body["build_time"] == "unknown"


def test_health_reads_env_variables(client, monkeypatch):
    """After setting the environment variable, `/health` should return the corresponding value"""
    monkeypatch.setenv("GIT_COMMIT", "abc1234")
    monkeypatch.setenv("APP_ENV", "staging")
    monkeypatch.setenv("BUILD_TIME", "2026-10-13T00:00:00Z")

    body = client.get("/health").json()
    assert body["commit"] == "abc1234"
    assert body["environment"] == "staging"
    assert body["build_time"] == "2026-10-13T00:00:00Z"