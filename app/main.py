import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from prometheus_fastapi_instrumentator import Instrumentator

from app import db
from app.dashboard import render_dashboard

logger = logging.getLogger("uvicorn.error")


def current_info() -> dict:
    return {
        "status": "ok",
        "commit": os.getenv("GIT_COMMIT", "unknown"),
        "environment": os.getenv("APP_ENV", "dev"),
        "build_time": os.getenv("BUILD_TIME", "unknown"),
    }


@asynccontextmanager
async def lifespan(app: FastAPI):
    # One row per container start. A database problem is logged but must never take /health down.
    try:
        info = current_info()
        db.record_deployment(info["commit"], info["environment"], info["build_time"])
    except Exception:
        logger.exception("could not record deployment")
    yield


app = FastAPI(title="Build Status Dashboard", lifespan=lifespan)


@app.get("/health")
def health():
    return current_info()


@app.get("/", response_class=HTMLResponse)
def dashboard():
    try:
        history = db.get_history()
    except Exception:
        logger.exception("could not read deployment history")
        history = []
    return render_dashboard(current_info(), history)


# Prometheus metrics at /metrics, including HTTP request latency
Instrumentator().instrument(app).expose(app, endpoint="/metrics")