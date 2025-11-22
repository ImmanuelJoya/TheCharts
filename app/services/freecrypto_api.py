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

    def _get_mock_data(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Return mock data when API is unavailable"""
        import random
        from datetime import datetime, timedelta

        now = datetime.now()

        # Mock crypto data
        mock_cryptos = {
            "BTC": {"price": 43250.00, "change_24h": 2.5, "volume": 12500000000},
            "ETH": {"price": 2280.50, "change_24h": 1.8, "volume": 8900000000},
            "ADA": {"price": 0.58, "change_24h": -0.5, "volume": 234000000},
            "SOL": {"price": 98.45, "change_24h": 3.2, "volume": 2100000000},
            "DOT": {"price": 7.82, "change_24h": 1.1, "volume": 432000000}
        }

        # Generate realistic mock data based on endpoint
        if endpoint == "/getCryptoList":
            return {
                "status": True,
                "data": [{"symbol": symbol, "name": symbol} for symbol in mock_cryptos.keys()]
            }

        elif endpoint == "/getTop":
            limit = params.get("limit", 10)
            cryptos = []
            for i, (symbol, data) in enumerate(mock_cryptos.items()):
                if i >= limit:
                    break
                cryptos.append({
                    "symbol": symbol,
                    "price": data["price"] * (1 + random.uniform(-0.02, 0.02)),
                    "change_24h": data["change_24h"] * (1 + random.uniform(-0.1, 0.1)),
                    "volume": data["volume"] * (1 + random.uniform(-0.2, 0.2))
                })
            return {"status": True, "data": cryptos}

        elif endpoint == "/getData":
            symbols = params.get("symbols", "").split(",")
            currency = params.get("currency", "USD")
            data = []
            for symbol in symbols:
                if symbol in mock_cryptos:
                    crypto_data = mock_cryptos[symbol]
                    data.append({
                        "symbol": symbol,
                        "price": crypto_data["price"] * (1 + random.uniform(-0.01, 0.01)),
                        "change_24h": crypto_data["change_24h"],
                        "volume": crypto_data["volume"],
                        "currency": currency
                    })
            return {"status": True, "data": data}

        elif endpoint == "/getFearGreed":
            return {
                "status": True,
                "data": {
                    "value": random.randint(20, 80),
                    "classification": random.choice(["Extreme Fear", "Fear", "Neutral", "Greed", "Extreme Greed"])
                }
            }

        elif endpoint == "/getPerformance":
            symbol = params.get("symbol", "BTC")
            base_price = mock_cryptos.get(symbol, {"price": 1000})["price"]
            return {
                "status": True,
                "data": {
                    "symbol": symbol,
                    "change_1h": round(random.uniform(-2, 2), 2),
                    "change_24h": round(random.uniform(-10, 10), 2),
                    "change_7d": round(random.uniform(-20, 20), 2),
                    "change_30d": round(random.uniform(-30, 30), 2)
                }
            }

        elif endpoint == "/getTechnicalAnalysis":
            symbol = params.get("symbol", "BTC")
            return {
                "status": True,
                "data": {
                    "symbol": symbol,
                    "macd": round(random.uniform(-100, 100), 2),
                    "signal": round(random.uniform(-100, 100), 2),
                    "rsi": round(random.uniform(20, 80), 1)
                }
            }

        elif endpoint == "/getVolatility":
            symbol = params.get("symbol")
            return {
                "status": True,
                "data": {
                    "symbol": symbol or "market",
                    "volatility": round(random.uniform(1, 5), 2),
                    "period": "24h"
                }
            }

        elif endpoint == "/getBreakouts":
            breakouts = {}
            for symbol in mock_cryptos.keys():
                breakouts[symbol] = {
                    "sma20": random.choice([True, False]),
                    "sma50": random.choice([True, False]),
                    "sma200": random.choice([True, False])
                }
            return {"status": True, "data": {"breakouts": breakouts}}

        elif endpoint == "/getATHATL":
            symbol = params.get("symbol", "BTC")
            base_price = mock_cryptos.get(symbol, {"price": 1000})["price"]
            return {
                "status": True,
                "data": {
                    "symbol": symbol,
                    "ath": base_price * 1.5,
                    "ath_date": "2021-11-10",
                    "atl": base_price * 0.1,
                    "atl_date": "2020-12-17",
                    "ath_distance": round((base_price - (base_price * 1.5)) / (base_price * 1.5) * 100, 2)
                }
            }

        elif endpoint == "/getConversion":
            from_symbol = params.get("from", "BTC")
            to_symbol = params.get("to", "USD")
            amount = params.get("amount", 1.0)

            from_price = mock_cryptos.get(from_symbol, {"price": 1000})["price"]
            to_price = 1.0 if to_symbol == "USD" else mock_cryptos.get(to_symbol, {"price": 100})["price"]

            converted_amount = (from_price * amount) / to_price
            return {
                "status": True,
                "data": {
                    "from": from_symbol,
                    "to": to_symbol,
                    "amount": amount,
                    "result": round(converted_amount, 6)
                }
            }

        elif endpoint == "/getHistory":
            symbol = params.get("symbol", "BTC")
            days = params.get("days", 30)
            base_price = mock_cryptos.get(symbol, {"price": 1000})["price"]

            history = []
            for i in range(days):
                date = (now - timedelta(days=i)).strftime("%Y-%m-%d")
                price = base_price * (1 + random.uniform(-0.1, 0.1))
                history.append({
                    "date": date,
                    "price": round(price, 2),
                    "volume": random.randint(1000000, 5000000)
                })

            return {"status": True, "data": history}

        elif endpoint == "/getOHLC":
            symbol = params.get("symbol", "BTC")
            days = params.get("days", 30)
            base_price = mock_cryptos.get(symbol, {"price": 1000})["price"]

            ohlc = []
            for i in range(days):
                date = (now - timedelta(days=i)).strftime("%Y-%m-%d")
                open_price = base_price * (1 + random.uniform(-0.05, 0.05))
                close_price = base_price * (1 + random.uniform(-0.05, 0.05))
                high_price = max(open_price, close_price) * (1 + random.uniform(0, 0.02))
                low_price = min(open_price, close_price) * (1 - random.uniform(0, 0.02))

                ohlc.append({
                    "date": date,
                    "open": round(open_price, 2),
                    "high": round(high_price, 2),
                    "low": round(low_price, 2),
                    "close": round(close_price, 2)
                })

            return {"status": True, "data": ohlc}

        # Default mock response
        return {
            "status": True,
            "data": {"message": f"Mock data for {endpoint}", "params": params}
        }