from pydantic import BaseModel
from app.schemas.base import IdBase

__all__ = ["Author", "GetAuthorsResponse", "CreateAuthorResponse", "CreateAuthorRequest"]


class Author(IdBase):
    name: str
    pseudonym: str


class GetAuthorsResponse(BaseModel):
    items: list[Author]
    total_count: int


class CreateAuthorRequest(BaseModel):
    name: str
    pseudonym: str


class CreateAuthorResponse(BaseModel):
    message: str
