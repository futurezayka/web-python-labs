from uuid import UUID

from app.schemas import CreateGenreRequest, CreateGenreResponse
from app.uow.sql import SQLUnitOfWork


class GenreService:
    @staticmethod
    async def create_genre(request: CreateGenreRequest, uow: SQLUnitOfWork) -> CreateGenreResponse:
        async with uow:
            await uow.genres.create(obj_in=request.model_dump())
        return CreateGenreResponse(message="Genre created")

    @staticmethod
    async def get_genres(page: int, per_page: int, uow: SQLUnitOfWork):
        async with uow:
            genres = await uow.genres.get_multi(offset=page, limit=per_page)
        return genres

    @staticmethod
    async def delete_genre(id: UUID, uow: SQLUnitOfWork):
        async with uow:
            await uow.genres.delete(filters={"id": id})
