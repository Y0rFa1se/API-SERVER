from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from .web_modules.api_requests import get_files_ls

import os

router = APIRouter()
app = FastAPI()

templates = Jinja2Templates(directory="templates/files")

@router.get("/authentification", response_class=HTMLResponse)
async def authentification(request: Request):
    return templates.TemplateResponse("authentification.html", {"request": request})

@router.get("/ls", response_class=HTMLResponse)
async def web_get_stock_tickers(request: Request):
    password = request.cookies.get("password")
    if password == os.getenv("GUEST_PASSWORD"):
        files = await get_files_ls()

        return templates.TemplateResponse("ls.html", {"request": request, "files": files["list"], "password": password})
    
    else:
        return RedirectResponse(url="/files/authentification")
    
@router.get("/download/{file_name}", response_class=HTMLResponse)
async def web_get_stock_prices(request: Request, file_name: str):
    password = request.cookies.get("password")
    if password == os.getenv("GUEST_PASSWORD"):
        return templates.TemplateResponse("download.html", {"request": request, "file_name": file_name, "password": password})
    
    else:
        return RedirectResponse(url="/files/authentification")
    
@router.get("/upload", response_class=HTMLResponse)
async def web_get_stock_prices(request: Request):
    password = request.cookies.get("password")
    if password == os.getenv("GUEST_PASSWORD"):
        return templates.TemplateResponse("upload.html", {"request": request, "password": password})
    
    else:
        return RedirectResponse(url="/files/authentification")
    
@router.get("/delete/{file_name}", response_class=HTMLResponse)
async def web_get_stock_prices(request: Request, file_name: str):
    password = request.cookies.get("password")
    if password == os.getenv("GUEST_PASSWORD"):
        return templates.TemplateResponse("delete.html", {"request": request, "file_name": file_name, "password": password})
    
    else:
        return RedirectResponse(url="/files/authentification")