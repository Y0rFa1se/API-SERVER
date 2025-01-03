from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/ping")
async def ping():
    return {"response": "pong"}

@router.get("/error")
async def error():
    raise HTTPException(status_code=400, detail="Intentional error")