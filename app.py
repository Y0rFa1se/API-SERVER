from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os

from routes.test import router as test_router
from routes.api import router as api_router
from routes.web import router as web_router

load_dotenv()

os.makedirs("../../storage/api_server_files", exist_ok=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처 허용 (보안상 주의)
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(test_router, prefix="/test")
app.include_router(api_router, prefix="/api")
app.include_router(web_router)