from app.managers.convert import ConvertManager
from app.mongo_repositories.base import RepositoryMixin


class UserRepository(RepositoryMixin):
    collection_name = "users"
    convert_manager = ConvertManager()

    async def get(self, filters: dict[str, any]):
        user = await super().get(filters)
        return self.convert_manager.convert_user(user)
