from fastapi import APIRouter
from .config import router as config_router
from .files import router as files_router
from .gpt import router as gpt_router
from .mariadb import router as mariadb_router
from .pychess import router as pychess_router

router = APIRouter()
router.include_router(config_router, tags=["config"])
router.include_router(files_router, prefix="/files", tags=["files"])
router.include_router(gpt_router, prefix="/gpt", tags=["gpt"])
router.include_router(mariadb_router, prefix="/mariadb", tags=["mariadb"])
router.include_router(pychess_router, prefix="/chess", tags=["chess"])