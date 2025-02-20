from loguru import logger

from app.infra.database import get_session_maker
from app.repositories.author import AuthorRepository
from app.repositories.book import BookRepository
from app.repositories.genre import GenreRepository
from app.repositories.user import UserRepository
from app.uow.base import ABCUnitOfWork


class SQLUnitOfWork(ABCUnitOfWork):
    def __init__(self) -> None:
        self.session_maker = get_session_maker()

    async def __aenter__(self) -> "SQLUnitOfWork":
        self.session = self.session_maker()
        self.users = UserRepository(self.session)
        self.genres = GenreRepository(self.session)
        self.books = BookRepository(self.session)
        self.authors = AuthorRepository(self.session)
        return self

    async def __aexit__(self, exc_type: any, exc: any, tb: any) -> None:
        if exc:
            logger.exception("An error occurred while processing the request. Rolling back. Error: {exc}", exc=exc)
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()
        await logger.complete()

        if exc:
            raise exc

    async def rollback(self):
        await self.session.rollback()
