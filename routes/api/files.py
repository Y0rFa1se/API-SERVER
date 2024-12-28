from fastapi import APIRouter, UploadFile
from .api_modules.files import upload, download, delete, list_files

router = APIRouter()

@router.get("/ls")
async def ls(password: str):
    return await list_files(password)

@router.post("/upload")
async def upload_file(file: UploadFile, password: str):
    return await upload(file, password)

@router.get("/download/{file_name}")
async def download_file(file_name: str, password: str):
    return await download(file_name, password)

@router.get("/delete/{file_name}")
async def delete_file(file_name: str, password: str):
    return await delete(file_name, password)