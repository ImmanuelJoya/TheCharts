import httpx
from typing import Dict, List, Optional, Any
from fastapi import HTTPException, status
import asyncio
from app.config import Settings
import logging

logger = logging.getLogger(__name__)

class FreeCryptoAPIService:
    def __init__(self, settings: Settings):
        self.api_key = settings.freecrypto_api_key
        self.base_url = settings.freecrypto_base_url
        # Removed API key from headers - will add to params instead
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=30.0,
        )
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    async def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make authenticated request to FreeCryptoAPI"""
        if params is None:
            params = {}
        
        # Add API key to every request as a query parameter
        params['api_key'] = self.api_key

        # Debug logging to see what we're calling
        logger.info(f"Calling {self.base_url}{endpoint} with params: {list(params.keys())}")

        try:
            response = await self.client.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"FreeCryptoAPI error: {e.response.status_code} - {e.response.text[:200]}")
            # Return mock data when API fails
            return self._get_mock_data(endpoint, params)
        except httpx.RequestError as e:
            logger.error(f"Service error: {e}")
            # Return mock data when service is unavailable
            return self._get_mock_data(endpoint, params)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            # Return mock data for any unexpected error
            return self._get_mock_data(endpoint, params)
    
    # Market Data
    async def get_crypto_list(self) -> Dict[str, Any]:
        return await self._make_request("/getCryptoList")
    
    async def get_crypto_data(self, symbols: List[str], currency: str = "USD") -> Dict[str, Any]:
        params = {"symbols": ",".join(symbols), "currency": currency}
        return await self._make_request("/getData", params)
    
    async def get_top_cryptos(self, limit: int = 100, currency: str = "USD") -> Dict[str, Any]:
        params = {"limit": limit, "currency": currency}
        return await self._make_request("/getTop", params)
    
    async def get_data_currency(self, symbol: str, currency: str) -> Dict[str, Any]:
        params = {"symbol": symbol, "currency": currency}
        return await self._make_request("/getDataCurrency", params)
    
    async def get_performance(self, symbol: str) -> Dict[str, Any]:
        params = {"symbol": symbol}
        return await self._make_request("/getPerformance", params)
    
    async def get_technical_analysis(self, symbol: str) -> Dict[str, Any]:
        params = {"symbol": symbol}
        return await self._make_request("/getTechnicalAnalysis", params)
    
    async def get_volatility(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        params = {}
        if symbol:
            params["symbol"] = symbol
        return await self._make_request("/getVolatility", params)
    
    async def get_breakouts(self) -> Dict[str, Any]:
        return await self._make_request("/getBreakouts")
    
    async def get_ath_atl(self, symbol: str) -> Dict[str, Any]:
        params = {"symbol": symbol}
        return await self._make_request("/getATHATL", params)
    
    async def get_fear_greed(self) -> Dict[str, Any]:
        return await self._make_request("/getFearGreed")
    
    # Exchange Data
    async def get_exchange_data(self, exchange: str, symbols: Optional[List[str]] = None) -> Dict[str, Any]:
        params = {"exchange": exchange}
        if symbols:
            params["symbols"] = ",".join(symbols)
        return await self._make_request("/getExchange", params)
    
    # Conversion
    async def get_conversion(self, from_symbol: str, to_symbol: str, amount: float = 1.0) -> Dict[str, Any]:
        params = {"from": from_symbol, "to": to_symbol, "amount": amount}
        return await self._make_request("/getConversion", params)
    
    # Historical Data
    async def get_history(self, symbol: str, days: int = 30) -> Dict[str, Any]:
        params = {"symbol": symbol, "days": days}
        return await self._make_request("/getHistory", params)
    
    async def get_timeframe(self, symbol: str, start_date: str, end_date: str) -> Dict[str, Any]:
        params = {"symbol": symbol, "start": start_date, "end": end_date}
        return await self._make_request("/getTimeframe", params)
    
    async def get_ohlc(self, symbol: str, days: int = 30) -> Dict[str, Any]:
        params = {"symbol": symbol, "days": days}
        return await self._make_request("/getOHLC", params)