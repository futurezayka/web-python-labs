from core.api.repositories.book import book_repository
from core.api.serializers.book import CreateBookSerializer, BookSerializer
from core.api.views.base import BaseModelViewSet


class BookViewSet(BaseModelViewSet):
    def get_queryset(self):
        return book_repository.get_all()

    def get_serializer_class(self):
        if self.action == "create":
            return CreateBookSerializer
        return BookSerializer
