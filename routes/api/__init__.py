from fastapi import APIRouter
from .config import router as config_router

router = APIRouter()
router.include_router(config_router, tags=["config"])