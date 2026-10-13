# pytest 通用夹具：为后续单元 / 集成 / E2E 测试提供可复用的测试客户端
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """返回一个基于当前应用的 TestClient，测试无需重复构造应用实例。"""
    return TestClient(app)