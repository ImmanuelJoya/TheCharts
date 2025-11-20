from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from app.services.freecrypto_api import FreeCryptoAPIService
from app.repositories.crypto_repository import CryptoRepository
from app.models.schemas import *
from app.config import get_settings
from app.dependencies import get_api_service, get_crypto_repository

router = APIRouter(prefix="/market", tags=["Market Data"])

@router.get("/list", response_model=CryptoListResponse)
async def get_crypto_list(
    api: FreeCryptoAPIService = Depends(get_api_service)
):
    """Get list of supported crypto currencies and pairs"""
    return await api.get_crypto_list()

@router.post("/data", response_model=CryptoDataResponse)
async def get_crypto_data(
    request: CryptoDataRequest,
    api: FreeCryptoAPIService = Depends(get_api_service)
):
    """Get single or multiple crypto currency data"""
    return await api.get_crypto_data(request.symbols, request.currency)

@router.get("/top", response_model=List[TopCryptoResponse])
async def get_top_cryptos(
    limit: int = Query(100, ge=1, le=500),
    currency: str = Query("USD"),
    repo: CryptoRepository = Depends(get_crypto_repository)
):
    """Get ranked coins merged with live data"""
    return await repo.get_top_cryptos_with_details(limit, currency)

@router.get("/performance", response_model=PerformanceResponse)
async def get_performance(
    symbol: str = Query(..., description="Crypto symbol"),
    api: FreeCryptoAPIService = Depends(get_api_service)
):
    """Get performance change percentages for a symbol"""
    return await api.get_performance(symbol)

@router.get("/technical-analysis", response_model=TechnicalAnalysisResponse)
async def get_technical_analysis(
    symbol: str = Query(..., description="Crypto symbol"),
    api: FreeCryptoAPIService = Depends(get_api_service)
):
    """Get technical analysis (MACD, signal line, RSI) for a symbol"""
    data = await api.get_technical_analysis(symbol)
    # Transform data to match schema
    return {
        "symbol": symbol,
        "macd": data.get("macd", 0),
        "signal_line": data.get("signal", 0),
        "rsi": data.get("rsi", 0),
        "timestamp": datetime.now()
    }

@router.get("/volatility", response_model=VolatilityResponse)
async def get_volatility(
    symbol: Optional[str] = Query(None, description="Crypto symbol or none for top coins"),
    api: FreeCryptoAPIService = Depends(get_api_service)
):
    """Get volatility (standard deviation of price)"""
    data = await api.get_volatility(symbol)
    return {
        "symbol": symbol or "top",
        "volatility": data.get("volatility", 0),
        "period": data.get("period", "24h")
    }

@router.get("/breakouts", response_model=List[BreakoutResponse])
async def get_breakouts(
    api: FreeCryptoAPIService = Depends(get_api_service)
):
    """Get 20/50/200-SMA breakout signals"""
    data = await api.get_breakouts()
    # Transform to list format
    breakouts = []
    for symbol, signals in data.get("breakouts", {}).items():
        breakouts.append({
            "symbol": symbol,
            "signals": {
                "sma_20": signals.get("sma20", False),
                "sma_50": signals.get("sma50", False),
                "sma_200": signals.get("sma200", False)
            }
        })
    return breakouts

@router.get("/ath-atl", response_model=ATHATLResponse)
async def get_ath_atl(
    symbol: str = Query(..., description="Crypto symbol"),
    api: FreeCryptoAPIService = Depends(get_api_service)
):
    """Get all-time high/low, dates, distance from ATH, multipliers"""
    return await api.get_ath_atl(symbol)

@router.get("/fear-greed", response_model=FearGreedResponse)
async def get_fear_greed(
    api: FreeCryptoAPIService = Depends(get_api_service)
):
    """Get Fear & Greed Index"""
    data = await api.get_fear_greed()
    return {
        "value": data.get("value", 50),
        "classification": data.get("classification", "Neutral"),
        "timestamp": datetime.now()
    }