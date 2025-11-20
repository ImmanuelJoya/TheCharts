import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
import json

def test_health_endpoint(client: TestClient):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root_endpoint(client: TestClient):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "Crypto Real-Time Monitoring Platform API" in data["message"]

@patch("app.services.freecrypto_api.FreeCryptoAPIService._make_request", new_callable=AsyncMock)
def test_get_crypto_list_smoke(mock_api, client: TestClient):
    """Test market data endpoint smoke test"""
    mock_api.return_value = {
        "symbols": ["BTC", "ETH", "ADA"],
        "pairs": {"BTC": "Bitcoin", "ETH": "Ethereum"}
    }
    
    response = client.get("/market/list")
    assert response.status_code == 200
    data = response.json()
    assert "symbols" in data
    assert "pairs" in data

@patch("app.services.freecrypto_api.FreeCryptoAPIService._make_request", new_callable=AsyncMock)
def test_get_top_cryptos_smoke(mock_api, client: TestClient):
    """Test top cryptos endpoint"""
    mock_api.return_value = {
        "data": [
            {"symbol": "BTC", "name": "Bitcoin", "price": 45000, "market_cap": 850000000000}
        ]
    }
    
    response = client.get("/market/top?limit=10")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@patch("app.services.freecrypto_api.FreeCryptoAPIService._make_request", new_callable=AsyncMock)
def test_get_performance_smoke(mock_api, client: TestClient):
    """Test performance endpoint"""
    mock_api.return_value = {
        "symbol": "BTC",
        "performance": {"1d": 2.5, "7d": 5.0, "30d": 15.0}
    }
    
    response = client.get("/market/performance?symbol=BTC")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "BTC"
    assert "performance" in data

@patch("app.services.freecrypto_api.FreeCryptoAPIService._make_request", new_callable=AsyncMock)
def test_get_fear_greed_smoke(mock_api, client: TestClient):
    """Test fear & greed endpoint"""
    mock_api.return_value = {
        "value": 75,
        "classification": "Greed"
    }
    
    response = client.get("/market/fear-greed")
    assert response.status_code == 200
    data = response.json()
    assert "value" in data
    assert "classification" in data

@patch("app.services.freecrypto_api.FreeCryptoAPIService._make_request", new_callable=AsyncMock)
def test_convert_smoke(mock_api, client: TestClient):
    """Test conversion endpoint"""
    mock_api.return_value = {
        "from": "BTC",
        "to": "USD",
        "amount": 1.0,
        "result": 45000,
        "rate": 45000
    }
    
    response = client.get("/conversion/convert?from_symbol=BTC&to_symbol=USD&amount=1")
    assert response.status_code == 200
    data = response.json()
    assert data["from_symbol"] == "BTC"
    assert data["to_symbol"] == "USD"

def test_websocket_connection(client: TestClient):
    """Test WebSocket endpoint is accessible"""
    # Note: This is a basic connectivity test
    # Full WebSocket testing requires a different approach
    response = client.get("/ws")
    # Socket.IO endpoint returns 400 without proper handshake, which is expected
    assert response.status_code in [200, 400, 403]

@pytest.mark.asyncio
@patch("app.services.freecrypto_api.FreeCryptoAPIService._make_request", new_callable=AsyncMock)
async def test_api_client_error_handling(mock_api):
    """Test API error handling"""
    from app.services.freecrypto_api import FreeCryptoAPIService
    from app.config import Settings
    
    mock_api.side_effect = Exception("API Error")
    
    settings = Settings(freecrypto_api_key="test", freecrypto_base_url="https://test.com")
    service = FreeCryptoAPIService(settings)
    
    with pytest.raises(Exception):
        await service.get_crypto_list()