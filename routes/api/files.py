from fastapi import APIRouter, UploadFile
from .api_modules.files import upload, download

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile, password: str):
    return await upload(file, password)

@router.get("/download")
async def download_file(file_path: str, password: str):
    return await download(file_path, password)