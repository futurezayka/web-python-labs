from pydantic import BaseModel

__all__ = ["Author", "GetAuthorsResponse", "CreateAuthorResponse", "CreateAuthorRequest"]


class Author(BaseModel):
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
