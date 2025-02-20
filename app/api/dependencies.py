from typing import Annotated

from fastapi import Depends

from app.schemas import User
from app.services.auth import AuthService
from app.services.author import AuthorService
from app.services.book import BookService
from app.services.genre import GenreService
from app.uow.base import ABCUnitOfWork
from app.uow.sql import SQLUnitOfWork

__all__ = [
    "SQLUnitOfWorkDep",
    "auth_service",
    "current_user",
    "admin_user",
    "author_service",
    "book_service",
    "genre_service",
]

SQLUnitOfWorkDep = Annotated[ABCUnitOfWork, Depends(SQLUnitOfWork)]
auth_service = Annotated[AuthService, Depends(AuthService)]
current_user = Annotated[User, Depends(AuthService.get_current_user)]
admin_user = Annotated[User, Depends(AuthService.get_admin_user)]
author_service = Annotated[AuthorService, Depends(AuthorService)]
book_service = Annotated[BookService, Depends(BookService)]
genre_service = Annotated[GenreService, Depends(GenreService)]
