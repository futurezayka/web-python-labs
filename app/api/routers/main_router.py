from fastapi import APIRouter

from app.api.routers.auth import router as auth_router
from app.api.routers.author import router as author_router
from app.api.routers.genre import router as genre_router
from app.api.routers.book import router as book_router

__all__ = ["router"]

router = APIRouter(prefix="/api")
router.include_router(auth_router)
router.include_router(author_router)
router.include_router(genre_router)
router.include_router(book_router)
