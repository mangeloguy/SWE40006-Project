
def test_metrics_returns_ok(client):
    """GET /metrics returns 200"""
    resp = client.get("/metrics")
    assert resp.status_code == 200


def test_metrics_are_prometheus_text(client):
    """The response should be in the Prometheus text format (text/plain)"""
    resp = client.get("/metrics")
    assert "text/plain" in resp.headers["content-type"]


def test_metrics_include_http_latency(client):
    """The metrics should include HTTP request latency metrics"""
    body = client.get("/metrics").text
    assert "http_request_duration_seconds" in body
    assert "http_requests_total" in body