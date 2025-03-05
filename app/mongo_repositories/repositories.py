from motor.motor_asyncio import AsyncIOMotorDatabase
from app.managers.convert import ConvertManager
from app.mongo_repositories.base import RepositoryMixin

class AuthorRepository(RepositoryMixin):
    collection_name = "authors"
    convert_manager = ConvertManager()

    async def get_multi(self, offset: int = 0, limit: int = 10, **filters: any):
        items = await super().get_multi(offset=offset, limit=limit, **filters)
        return {"items": [self.convert_manager.convert_author(author) for author in items], "total_count": len(items)}

class BookRepository(RepositoryMixin):
    collection_name = "books"
    convert_manager = ConvertManager()

    async def get_multi(self, offset: int = 0, limit: int = 10, **filters: any):
        items = await super().get_multi(offset=offset, limit=limit, **filters)
        return {"items": [self.convert_manager.convert_book(book) for book in items], "total_count": len(items)}

class GenreRepository(RepositoryMixin):
    collection_name = "genres"
    convert_manager = ConvertManager()

    async def get_multi(self, offset: int = 0, limit: int = 10, **filters: any):
        items = await super().get_multi(offset=offset, limit=limit, **filters)
        return {"items": [self.convert_manager.convert_genre(genre) for genre in items], "total_count": len(items)}

class UserRepository(RepositoryMixin):
    collection_name = "users"
    convert_manager = ConvertManager()

    async def get(self, filters: dict[str, any]):
        user = await super().get(filters)
        return self.convert_manager.convert_user(user)
