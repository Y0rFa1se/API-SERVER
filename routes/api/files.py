from fastapi import APIRouter, UploadFile
from .api_modules.files import upload, download, download_stockdb

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile, password: str):
    return await upload(file, password)

@router.get("/download")
async def download_file(file_path: str, password: str):
    return await download(file_path, password)

@router.get("/download_stockdb")
async def download_stockdb_file(password: str):
    return await download_stockdb(password)