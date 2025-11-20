import httpx
from typing import Dict, List, Optional, Any
from fastapi import HTTPException, status
import asyncio
from app.config import Settings

class FreeCryptoAPIService:
    def __init__(self, settings: Settings):
        self.api_key = settings.freecrypto_api_key
        self.base_url = settings.freecrypto_base_url
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=30.0,
            headers={"X-API-KEY": self.api_key}
        )
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    async def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make authenticated request to FreeCryptoAPI"""
        try:
            response = await self.client.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"FreeCryptoAPI error: {e.response.text}"
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Service unavailable: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}"
            )
    
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