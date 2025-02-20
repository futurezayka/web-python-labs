from uuid import UUID

from app import schemas
from app.uow.sql import SQLUnitOfWork


class AuthorService:
    @staticmethod
    async def create_author(request: schemas.CreateAuthorRequest, uow: SQLUnitOfWork) -> schemas.CreateAuthorResponse:
        async with uow:
            await uow.authors.create(obj_in=request.model_dump())
        return schemas.CreateAuthorResponse(message="Author created")

    @staticmethod
    async def get_authors(page: int, per_page: int, uow: SQLUnitOfWork) -> schemas.GetAuthorsResponse:
        async with uow:
            authors = await uow.authors.get_multi(offset=page, limit=per_page)
        return authors

    @staticmethod
    async def delete_author(id: UUID, uow: SQLUnitOfWork):
        async with uow:
            await uow.authors.delete(filters={"id": id})
