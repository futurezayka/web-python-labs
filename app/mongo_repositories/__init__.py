from app.mongo_repositories.book import BookRepository
from app.mongo_repositories.genre import GenreRepository
from app.mongo_repositories.user import UserRepository
from app.mongo_repositories.author import AuthorRepository


__all__ = [
    "BookRepository",
    "GenreRepository",
    "UserRepository",
    "AuthorRepository",
]
