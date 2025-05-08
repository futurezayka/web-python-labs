from core.api.repositories.author import author_repository
from core.api.serializers.author import AuthorSerializer, AuthorCreateSerializer
from core.api.views.base import BaseModelViewSet


class AuthorViewSet(BaseModelViewSet):
    def get_queryset(self):
        return author_repository.get_all()

    def get_serializer_class(self):
        if self.action == "create":
            return AuthorCreateSerializer
        return AuthorSerializer
