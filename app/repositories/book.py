from app import models, schemas
from app.managers.convert import ConvertManager
from app.repositories.base import RepositoryMixin


class BookRepository(RepositoryMixin):
    model = models.Book
    convert_manager = ConvertManager()

    async def get_multi(
        self, offset: int = 0, limit: int = 10, order_by: str | None = None, **filters: any
    ) -> schemas.GetBooksResponse:
        items, count = await super().get_multi(offset=offset, limit=limit, order_by=order_by, **filters)
        return schemas.GetBooksResponse(
            items=[self.convert_manager.convert_book(book) for book in items], total_count=count
        )
