from app.mongo_repositories.base import RepositoryMixin


class AuthorRepository(RepositoryMixin):
    collection_name = "authors"

    async def get_multi(self, offset: int = 0, limit: int = 10, **filters: any):
        items = await super().get_multi(offset=offset, limit=limit, **filters)
        return items, len(items)
