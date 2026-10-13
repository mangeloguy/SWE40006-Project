# /health 端点的单元测试：验证状态码、字段结构与环境变量注入
def test_health_returns_ok(client):
    """GET /health 返回 200，且 status 字段为 ok。"""
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_health_defaults_when_env_unset(client, monkeypatch):
    """未设置相关环境变量时，各字段回退到默认值。"""
    monkeypatch.delenv("GIT_COMMIT", raising=False)
    monkeypatch.delenv("APP_ENV", raising=False)
    monkeypatch.delenv("BUILD_TIME", raising=False)

    body = client.get("/health").json()
    assert body["commit"] == "unknown"
    assert body["environment"] == "dev"
    assert body["build_time"] == "unknown"


def test_health_reads_env_variables(client, monkeypatch):
    """设置环境变量后，/health 应返回对应的值。"""
    monkeypatch.setenv("GIT_COMMIT", "abc1234")
    monkeypatch.setenv("APP_ENV", "staging")
    monkeypatch.setenv("BUILD_TIME", "2026-10-13T00:00:00Z")

    body = client.get("/health").json()
    assert body["commit"] == "abc1234"
    assert body["environment"] == "staging"
    assert body["build_time"] == "2026-10-13T00:00:00Z"