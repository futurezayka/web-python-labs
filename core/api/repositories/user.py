from core.api.models import User
from core.api.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    pass


user_repository = UserRepository(model=User)
