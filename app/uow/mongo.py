from loguru import logger
from app.mongo_repositories import UserRepository, GenreRepository, BookRepository, AuthorRepository
from app.uow.base import ABCUnitOfWork
from app.infra.database.mongodb import get_mongo_database


class MongoUnitOfWork(ABCUnitOfWork):
    def __init__(self) -> None:
        self.db = get_mongo_database()

    async def __aenter__(self) -> "MongoUnitOfWork":
        self.users = UserRepository(self.db)
        self.genres = GenreRepository(self.db)
        self.books = BookRepository(self.db)
        self.authors = AuthorRepository(self.db)
        return self

    async def __aexit__(self, exc_type: any, exc: any, tb: any) -> None:
        if exc:
            logger.exception("An error occurred while processing the request. Error: {exc}", exc=exc)
            raise exc

    async def rollback(self): ...
