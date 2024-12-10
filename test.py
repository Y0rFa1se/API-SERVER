from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os

from routes.api import router as api_router
from routes.web import router as web_router

app = FastAPI()

app.include_router(api_router, prefix="/api")
app.include_router(web_router)