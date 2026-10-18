
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Returns a TestClient based on the current application, eliminating the need to repeatedly construct application instances for testing."""
    return TestClient(app)