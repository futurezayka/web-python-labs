from core.api.models import Book
from core.api.repositories.base import BaseRepository


class BookRepository(BaseRepository[Book]):
    def get_all(self):
        return super().get_all().select_related("author", "genre")


book_repository = BookRepository(model=Book)
