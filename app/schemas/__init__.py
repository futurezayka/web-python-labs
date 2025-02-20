from app.schemas.author import Author, GetAuthorsResponse, CreateAuthorResponse, CreateAuthorRequest
from app.schemas.book import Book, GetBooksResponse, CreateBookRequest, CreateBookResponse, UpdateBookRequest
from app.schemas.genre import Genre, CreateGenreRequest, CreateGenreResponse, GetGenresResponse
from app.schemas.user import User

__all__ = [
    "User",
    "Author",
    "Book",
    "GetBooksResponse",
    "CreateBookRequest",
    "CreateBookResponse",
    "Genre",
    "GetAuthorsResponse",
    "CreateAuthorResponse",
    "CreateAuthorRequest",
    "CreateGenreRequest",
    "CreateGenreResponse",
    "GetGenresResponse",
    "UpdateBookRequest",
]
