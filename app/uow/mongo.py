from loguru import logger
from app.mongo_repositories.repositories import *
from app.uow.base import ABCUnitOfWork
from app.infra.database.mongodb import database 

class MongoUnitOfWork(ABCUnitOfWork):
    def __init__(self) -> None:
        self.db = database

    async def __aenter__(self) -> "MongoUnitOfWork":
        self.users = UserRepository(self.db)
        self.genres = GenreRepository(self.db)
        self.books = BookRepository(self.db)
        self.authors = AuthorRepository(self.db)
        return self

    async def __aexit__(self, exc_type: any, exc: any, tb: any) -> None:
        if exc:
            logger.exception("An error occurred while processing the request. Error: {exc}", exc=exc)

        if exc:
            raise exc

    async def rollback(self):
        """MongoDB не поддерживает традиционные транзакции, кроме реплицированных наборов."""
        logger.warning("Rollback is not supported in MongoDB.")
