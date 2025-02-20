from app import models, schemas
from app.managers.convert import ConvertManager
from app.repositories.base import RepositoryMixin


class UserRepository(RepositoryMixin):
    model = models.User
    convert_manager = ConvertManager()

    async def get(self, filters: dict[str, any]) -> schemas.User:
        user = await super().get(filters)
        return self.convert_manager.convert_user(user)
