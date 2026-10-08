import os

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Build Status Dashboard")


@app.get("/health")
def health():
    return {
        "status": "ok",
        "commit": os.getenv("GIT_COMMIT", "unknown"),
        "environment": os.getenv("APP_ENV", "dev"),
        "build_time": os.getenv("BUILD_TIME", "unknown"),
    }


# Prometheus metrics at /metrics, including HTTP request latency
Instrumentator().instrument(app).expose(app, endpoint="/metrics")