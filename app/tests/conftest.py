import pytest
from fastapi.testclient import TestClient
from app.main import create_app
from app.config import Settings
from unittest.mock import Mock

@pytest.fixture
def test_app():
    """Create test application"""
    return create_app()

@pytest.fixture
def client(test_app):
    """Create test client"""
    return TestClient(test_app)

@pytest.fixture
def mock_settings():
    """Mock settings for testing"""
    return Settings(
        freecrypto_api_key="test_api_key",
        freecrypto_base_url="https://mock-api.com",
        app_env="testing"
    )