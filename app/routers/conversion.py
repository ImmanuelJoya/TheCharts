from fastapi import APIRouter, Depends, Query
from app.services.freecrypto_api import FreeCryptoAPIService
from app.models.schemas import ConversionResponse
from app.dependencies import get_api_service

router = APIRouter(prefix="/conversion", tags=["Conversion"])

@router.get("/convert", response_model=ConversionResponse)
async def convert_crypto(
    from_symbol: str = Query(..., description="From symbol"),
    to_symbol: str = Query(..., description="To symbol"),
    amount: float = Query(1.0, description="Amount to convert"),
    api: FreeCryptoAPIService = Depends(get_api_service)
):
    """Convert between any 2 crypto currencies"""
    return await api.get_conversion(from_symbol, to_symbol, amount)