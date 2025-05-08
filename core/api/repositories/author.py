from core.api.models import Author
from core.api.repositories.base import BaseRepository


class AuthorRepository(BaseRepository[Author]):
    pass


author_repository = AuthorRepository(model=Author)
