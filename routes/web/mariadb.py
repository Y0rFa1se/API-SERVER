from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from .web_modules.api_requests import get_stock_tickers, get_stock_prices

import os

router = APIRouter()
app = FastAPI()

templates = Jinja2Templates(directory="templates/mariadb")

@router.get("/stock/authentification", response_class=HTMLResponse)
async def authentification(request: Request):
    return templates.TemplateResponse("authentification.html", {"request": request})

@router.get("/stock/tickers", response_class=HTMLResponse)
async def web_get_stock_tickers(request: Request):
    password = request.cookies.get("password")
    if password == os.getenv("GUEST_PASSWORD"):
        tickers = await get_stock_tickers()

        return templates.TemplateResponse("tickers.html", {"request": request, "tickers": tickers, "password": password})
    
    else:
        return RedirectResponse(url="/mariadb/stock/authentification")
    
@router.get("/stock/prices/{ticker}", response_class=HTMLResponse)
async def web_get_stock_prices(request: Request, ticker: str):
    password = request.cookies.get("password")
    if password == os.getenv("GUEST_PASSWORD"):
        prices = await get_stock_prices(ticker)

        return templates.TemplateResponse("prices.html", {"request": request, "prices": prices, "ticker": ticker, "password": password})
    
    else:
        return RedirectResponse(url="/mariadb/stock/authentification")