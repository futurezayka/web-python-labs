from core.api.models import Genre
from core.api.repositories.base import BaseRepository


class BookRepository(BaseRepository[Genre]):
    pass


genre_repository = BookRepository(model=Genre)
