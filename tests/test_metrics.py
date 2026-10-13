# /metrics 端点的测试：验证 Prometheus 指标暴露与 HTTP 延迟指标
def test_metrics_returns_ok(client):
    """GET /metrics 返回 200。"""
    resp = client.get("/metrics")
    assert resp.status_code == 200


def test_metrics_are_prometheus_text(client):
    """响应应为 Prometheus 文本格式(text/plain)。"""
    resp = client.get("/metrics")
    assert "text/plain" in resp.headers["content-type"]


def test_metrics_include_http_latency(client):
    """指标中应包含 HTTP 请求延迟指标（brief 3.5 要求）。"""
    body = client.get("/metrics").text
    assert "http_request_duration_seconds" in body
    assert "http_requests_total" in body