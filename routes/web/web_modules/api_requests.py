import httpx
import os

async def get_stock_tickers():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://localhost:8001/api/mariadb/stock/tickers?password={os.getenv('GUEST_PASSWORD')}")
        tickers = [row["Tables_in_stock_prices"].replace("_prices", "") for row in response.json()]

    return tickers

async def get_stock_prices(ticker):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://localhost:8001/api/mariadb/stock/prices/{ticker}?password={os.getenv('GUEST_PASSWORD')}")
        prices = response.json()

    return prices
