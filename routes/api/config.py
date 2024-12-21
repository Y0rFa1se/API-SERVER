from fastapi import APIRouter

router = APIRouter()

@router.get("/ping")
async def ping():
    return {"response": "pong!!"}

@router.get("/pong")
async def pong():
    return {"response": "ping!!"}