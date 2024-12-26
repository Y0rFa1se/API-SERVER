from fastapi import APIRouter, UploadFile
from .api_modules.mariadb import get_stock_prices, get_stock_tickers

router = APIRouter()

@router.get("/stock/tickers")
async def api_get_stock_tickers(password: str):
    return await get_stock_tickers(password)

@router.get("/stock/prices/{ticker}")
async def api_get_stock_prices(ticker: str, password: str):
    return await get_stock_prices(password, ticker)