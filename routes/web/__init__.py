from fastapi import APIRouter
from .main import router as main_router
from .mariadb import router as mariadb_router
from .files import router as files_router
from .pychess import router as pychess_router

router = APIRouter()
router.include_router(main_router)
router.include_router(mariadb_router, prefix="/mariadb", tags=["mariadb"])
router.include_router(files_router, prefix="/files", tags=["files"])
router.include_router(pychess_router, prefix="/chess", tags=["chess"])