from pydantic import BaseModel
from app.schemas.base import IdBase

__all__ = ["Genre", "GetGenresResponse", "CreateGenreRequest", "CreateGenreResponse"]


class Genre(IdBase):
    name: str


class GetGenresResponse(BaseModel):
    items: list[Genre]
    total_count: int


class CreateGenreRequest(BaseModel):
    name: str


class CreateGenreResponse(BaseModel):
    message: str
