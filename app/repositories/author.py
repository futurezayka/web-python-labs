from app import models, schemas
from app.managers.convert import ConvertManager
from app.repositories.base import RepositoryMixin


class AuthorRepository(RepositoryMixin):
    model = models.Author
    convert_manager = ConvertManager()

    async def get_multi(
        self, offset: int = 0, limit: int = 10, order_by: str | None = None, **filters: any
    ) -> schemas.GetAuthorsResponse:
        items, count = await super().get_multi(offset=offset, limit=limit, order_by=order_by, **filters)
        return schemas.GetAuthorsResponse(
            items=[self.convert_manager.convert_author(author) for author in items], total_count=count
        )
