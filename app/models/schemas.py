from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


# Common
class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None


# Market Data Schemas
class CryptoPair(BaseModel):
    symbol: str
    name: str
    currency: str
    price: float
    market_cap: Optional[float] = None
    volume_24h: Optional[float] = None
    change_24h: Optional[float] = None


class CryptoListResponse(BaseModel):
    symbols: List[str]
    pairs: Dict[str, Any]


class CryptoDataRequest(BaseModel):
    symbols: List[str] = Field(..., description="List of crypto symbols")
    currency: Optional[str] = "USD"


class CryptoDataResponse(BaseModel):
    data: Dict[str, CryptoPair]


class TopCryptoRequest(BaseModel):
    limit: int = Field(100, ge=1, le=500)
    currency: Optional[str] = "USD"


class TopCryptoResponse(BaseModel):
    rank: int
    symbol: str
    name: str
    price: float
    market_cap: float
    volume_24h: float
    change_24h: float


class PerformanceResponse(BaseModel):
    symbol: str
    performance: Dict[str, float]


class TechnicalAnalysisResponse(BaseModel):
    symbol: str
    macd: float
    signal_line: float
    rsi: float
    timestamp: datetime


class VolatilityResponse(BaseModel):
    symbol: str
    volatility: float
    period: str


class BreakoutSignals(BaseModel):
    sma_20: bool
    sma_50: bool
    sma_200: bool


class BreakoutResponse(BaseModel):
    symbol: str
    signals: BreakoutSignals


class ATHATLResponse(BaseModel):
    symbol: str
    ath: float
    ath_date: Optional[datetime]
    atl: float
    atl_date: Optional[datetime]
    distance_from_ath: float
    multipliers: Dict[str, float]


class FearGreedResponse(BaseModel):
    value: int
    classification: str
    timestamp: datetime


# Exchange Schemas
class ExchangeDataRequest(BaseModel):
    exchange: str
    symbols: Optional[List[str]] = None


class ExchangePair(BaseModel):
    symbol: str
    price: float
    volume: float
    bid: Optional[float] = None
    ask: Optional[float] = None


class ExchangeResponse(BaseModel):
    exchange: str
    pairs: Dict[str, ExchangePair]


# Conversion Schemas
class ConversionRequest(BaseModel):
    from_symbol: str
    to_symbol: str
    amount: float = 1.0


class ConversionResponse(BaseModel):
    from_symbol: str
    to_symbol: str
    amount: float
    result: float
    rate: float


# Historical Schemas
class HistoryRequest(BaseModel):
    symbol: str
    days: int = Field(30, ge=1, le=365)


class OHLCRequest(BaseModel):
    symbol: str
    days: int = Field(30, ge=1, le=365)


class OHLCData(BaseModel):
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: Optional[float] = None


class OHLCResponse(BaseModel):
    symbol: str
    data: List[OHLCData]


# WebSocket Schemas
class WSSubscribe(BaseModel):
    action: str = "subscribe"
    symbols: List[str]


class WSUnsubscribe(BaseModel):
    action: str = "unsubscribe"
    symbols: List[str]