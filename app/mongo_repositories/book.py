from app.mongo_repositories.base import RepositoryMixin


class BookRepository(RepositoryMixin):
    collection_name = "books"

    async def get_multi(self, offset: int = 0, limit: int = 10, **filters: any):
        items = await super().get_multi(offset=offset, limit=limit, **filters)
        return items, len(items)
