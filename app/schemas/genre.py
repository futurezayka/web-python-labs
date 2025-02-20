from pydantic import BaseModel

__all__ = ["Genre", "GetGenresResponse", "CreateGenreRequest", "CreateGenreResponse"]


class Genre(BaseModel):
    name: str


class GetGenresResponse(BaseModel):
    items: list[Genre]
    total_count: int


class CreateGenreRequest(BaseModel):
    name: str


class CreateGenreResponse(BaseModel):
    message: str
