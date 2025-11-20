from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.services.freecrypto_api import FreeCryptoAPIService
from app.models.schemas import HistoryRequest, OHLCResponse
from app.dependencies import get_api_service

router = APIRouter(prefix="/historical", tags=["Historical Data"])

@router.get("/history")
async def get_history(
    symbol: str = Query(..., description="Crypto symbol"),
    days: int = Query(30, ge=1, le=365, description="Number of days"),
    api: FreeCryptoAPIService = Depends(get_api_service)
):
    """Get last X days of historical data"""
    return await api.get_history(symbol, days)

@router.get("/timeframe")
async def get_timeframe(
    symbol: str = Query(..., description="Crypto symbol"),
    start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(..., description="End date (YYYY-MM-DD)"),
    api: FreeCryptoAPIService = Depends(get_api_service)
):
    """Get historical data within date range"""
    return await api.get_timeframe(symbol, start_date, end_date)

@router.get("/ohlc", response_model=OHLCResponse)
async def get_ohlc(
    symbol: str = Query(..., description="Crypto symbol"),
    days: int = Query(30, ge=1, le=365, description="Number of days"),
    api: FreeCryptoAPIService = Depends(get_api_service)
):
    """Get daily OHLC candles"""
    data = await api.get_ohlc(symbol, days)
    return {
        "symbol": symbol,
        "data": data.get("candles", [])
    }