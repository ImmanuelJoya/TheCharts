from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # API Configuration
    freecrypto_api_key: str
    freecrypto_base_url: str = "https://api.freecryptoapi.com"
    
    # Application Settings
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_env: str = "development"
    
    # WebSocket Settings
    ws_poll_interval: int = 30  # seconds between polls
    
    # Caching
    cache_ttl: int = 300  # seconds
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()