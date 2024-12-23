from fastapi import APIRouter, UploadFile
from .api_modules.gpt import render_requests, render_requests_with_image, openai_request

router = APIRouter()

@router.get("/request")
async def request_gpt(password: str, system: str, requests: str, model: str):
    query = await render_requests(system, requests)
    return await openai_request(password, query, model)