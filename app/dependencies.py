from functools import lru_cache
from app.config import Settings, get_settings
from app.services.freecrypto_api import FreeCryptoAPIService
from app.services.websocket_manager import WebSocketManager
from app.repositories.crypto_repository import CryptoRepository
from app.utils.cache import Cache

@lru_cache()
def get_api_service() -> FreeCryptoAPIService:
    settings = get_settings()
    return FreeCryptoAPIService(settings)

@lru_cache()
def get_cache() -> Cache:
    settings = get_settings()
    return Cache(settings.cache_ttl)

@lru_cache()
def get_crypto_repository() -> CryptoRepository:
    api_service = get_api_service()
    cache = get_cache()
    return CryptoRepository(api_service, cache)

@lru_cache()
def get_websocket_manager() -> WebSocketManager:
    return WebSocketManager()