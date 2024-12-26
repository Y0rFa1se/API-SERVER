from fastapi import APIRouter, UploadFile
from .api_modules.mariadb import get_stock_prices, get_stock_tickers

router = APIRouter()

@router.get("/stock/tickers")
async def query(password: str):
    return await get_stock_tickers(password)

@router.get("/stock/prices/{ticker}")
async def query(ticker: str, password: str):
    return await get_stock_prices(password, ticker)