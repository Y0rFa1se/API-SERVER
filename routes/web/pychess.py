from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

import os

router = APIRouter()
app = FastAPI()

templates = Jinja2Templates(directory="templates/chessboardjs-1.0.0")

@router.get("/authentication", response_class=HTMLResponse)
async def authentication(request: Request, referer: str = "/chess/play_with_gpt"):
    return templates.TemplateResponse("authentication.html", {"request": request, "referer": referer})

@router.get("/play_with_gpt", response_class=HTMLResponse)
async def web_play_with_gpt(request: Request):
    password = request.cookies.get("password")
    if password == os.getenv("GUEST_PASSWORD"):
        return templates.TemplateResponse("index.html", {"request": request, "password": password})
    
    else:
        return RedirectResponse(url="/chess/authentication")