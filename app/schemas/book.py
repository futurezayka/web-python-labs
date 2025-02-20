from uuid import UUID

from pydantic import BaseModel

from app.schemas.author import Author
from app.schemas.base import IdBase
from app.schemas.genre import Genre

__all__ = ["Book", "GetBooksResponse", "CreateBookRequest", "CreateBookResponse", "UpdateBookRequest"]


class Book(IdBase):
    author: Author
    genre: Genre
    title: str
    total_pages: int
    year: int


class GetBooksResponse(BaseModel):
    items: list[Book]
    total_count: int


class CreateBookRequest(BaseModel):
    author_id: UUID
    genre_id: UUID
    title: str
    total_pages: int
    year: int


class CreateBookResponse(BaseModel):
    message: str


class UpdateBookRequest(BaseModel):
    author_id: UUID | None = None
    genre_id: UUID | None = None
    title: str | None = None
    total_pages: int | None = None
    year: int | None = None
