from fastapi import APIRouter
from .main import router as main_router
from .mariadb import router as mariadb_router

router = APIRouter()
router.include_router(main_router)
router.include_router(mariadb_router, prefix="/mariadb", tags=["mariadb"])