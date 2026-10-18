import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app import db

logger = logging.getLogger("uvicorn.error")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # One row per container start. A database problem is logged but must never take /health down.
    try:
        db.record_deployment(
            os.getenv("GIT_COMMIT", "unknown"),
            os.getenv("APP_ENV", "dev"),
            os.getenv("BUILD_TIME", "unknown"),
        )
    except Exception:
        logger.exception("could not record deployment")
    yield


app = FastAPI(title="Build Status Dashboard", lifespan=lifespan)


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