from typing import Dict, List, Optional, Any
from app.services.freecrypto_api import FreeCryptoAPIService
from app.config import Settings
from app.utils.cache import Cache
import asyncio

class CryptoRepository:
    def __init__(self, api_service: FreeCryptoAPIService, cache: Cache):
        self.api = api_service
        self.cache = cache
    
    async def get_cached_crypto_data(self, symbols: List[str], currency: str = "USD") -> Dict[str, Any]:
        cache_key = f"crypto_data:{','.join(sorted(symbols))}:{currency}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached
        
        data = await self.api.get_crypto_data(symbols, currency)
        self.cache.set(cache_key, data)
        return data
    
    async def get_top_cryptos_with_details(self, limit: int = 100, currency: str = "USD") -> List[Dict[str, Any]]:
        cache_key = f"top_cryptos:{limit}:{currency}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached
        
        # Fetch top list and then get detailed data
        top_data = await self.api.get_top_cryptos(limit, currency)
        symbols = [item["symbol"] for item in top_data.get("data", [])[:10]]  # Limit for performance
        
        if symbols:
            details = await self.get_cached_crypto_data(symbols, currency)
            # Merge data
            merged = []
            for item in top_data.get("data", []):
                symbol = item["symbol"]
                if symbol in details.get("data", {}):
                    item.update(details["data"][symbol])
                merged.append(item)
            self.cache.set(cache_key, merged)
            return merged
        
        self.cache.set(cache_key, top_data.get("data", []))
        return top_data.get("data", [])
    
    async def get_real_time_update(self, symbols: List[str]) -> Dict[str, Any]:
        """Fetch real-time update for WebSocket broadcasting"""
        return await self.api.get_crypto_data(symbols)