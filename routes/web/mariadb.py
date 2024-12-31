from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from .web_modules.api_requests import get_stock_tickers, get_stock_prices

import os

router = APIRouter()
app = FastAPI()

templates = Jinja2Templates(directory="templates/mariadb")

@router.get("/stock/authentication", response_class=HTMLResponse)
async def authentication(request: Request, referer: str = "/mariadb/stock/tickers"):
    return templates.TemplateResponse("authentication.html", {"request": request, "referer": referer})

@router.get("/stock/tickers", response_class=HTMLResponse)
async def web_get_stock_tickers(request: Request):
    password = request.cookies.get("password")
    if password == os.getenv("GUEST_PASSWORD"):
        tickers = await get_stock_tickers()

        return templates.TemplateResponse("tickers.html", {"request": request, "tickers": tickers, "password": password})
    
    else:
        return RedirectResponse(url="/mariadb/stock/authentication?referer=/mariadb/stock/tickers")
    
@router.get("/stock/prices/{ticker}", response_class=HTMLResponse)
async def web_get_stock_prices(request: Request, ticker: str):
    password = request.cookies.get("password")
    if password == os.getenv("GUEST_PASSWORD"):
        prices = await get_stock_prices(ticker)

        return templates.TemplateResponse("prices.html", {"request": request, "prices": prices, "ticker": ticker, "password": password})
    
    else:
        return RedirectResponse(url="/mariadb/stock/authentication?referer=/mariadb/stock/prices/" + ticker)