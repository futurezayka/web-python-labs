from app import models, schemas
from app.managers.convert import ConvertManager
from app.repositories.base import RepositoryMixin
from app.uow.mongo import MongoUnitOfWork


class AuthorRepository(RepositoryMixin):
    model = models.Author
    convert_manager = ConvertManager()

    async def get_multi(
        self, offset: int = 0, limit: int = 10, order_by: str | None = None, **filters: any
    ) -> schemas.GetAuthorsResponse:
        async with MongoUnitOfWork() as mongo_uow:
            items, count = await mongo_uow.authors.get_multi(offset=offset, limit=limit, order_by=order_by, **filters)

        if not (items and count):
            items, count = await super().get_multi(offset=offset, limit=limit, order_by=order_by, **filters)

        return schemas.GetAuthorsResponse(
            items=[self.convert_manager.convert_author(author) for author in items], total_count=count
        )

    async def create(self, obj_in: dict[str, any]):
        async with MongoUnitOfWork() as mongo_uow:
            await mongo_uow.authors.create(obj_in)
        await super().create(obj_in)

    async def delete(self, filters: dict[str, any]):
        async with MongoUnitOfWork() as mongo_uow:
            await mongo_uow.authors.delete(filters)
        await super().delete(filters)
