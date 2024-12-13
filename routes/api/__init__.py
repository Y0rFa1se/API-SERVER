from fastapi import APIRouter
from .config import router as config_router
from .files import router as files_router

router = APIRouter()
router.include_router(config_router, tags=["config"])
router.include_router(files_router, prefix="/files", tags=["files"])