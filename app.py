from fastapi import FastAPI
from dotenv import load_dotenv
import os

from routes.test import router as test_router
from routes.api import router as api_router
from routes.web import router as web_router

load_dotenv()

os.makedirs("../../storage/api_server_files", exist_ok=True)

app = FastAPI()

app.include_router(test_router, prefix="/test")
app.include_router(api_router, prefix="/api")
app.include_router(web_router)