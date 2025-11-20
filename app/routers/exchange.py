from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from app.services.freecrypto_api import FreeCryptoAPIService
from app.models.schemas import ExchangeResponse, ExchangeDataRequest
from app.dependencies import get_api_service

router = APIRouter(prefix="/exchange", tags=["Exchange Data"])

@router.get("/data", response_model=ExchangeResponse)
async def get_exchange_data(
    exchange: str = Query(..., description="Exchange name (e.g., binance, coinbase)"),
    symbols: Optional[List[str]] = Query(None, description="Optional list of symbols"),
    api: FreeCryptoAPIService = Depends(get_api_service)
):
    """Get all pairs and their latest data on a specific exchange"""
    return await api.get_exchange_data(exchange, symbols)