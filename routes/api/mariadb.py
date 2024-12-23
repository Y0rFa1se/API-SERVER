from fastapi import APIRouter, UploadFile
from .api_modules.mariadb import query_db

router = APIRouter()

@router.get("/query")
async def query(password: str, db_name: str, query: str):
    return await query_db(password, db_name, query)