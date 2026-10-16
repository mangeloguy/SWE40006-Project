
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """返回一个基于当前应用的 TestClient，测试无需重复构造应用实例。"""
    return TestClient(app)