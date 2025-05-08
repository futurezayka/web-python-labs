from core.api.repositories.genre import genre_repository
from core.api.serializers.genre import GenreSerializer, GenreCreateSerializer
from core.api.views.base import BaseModelViewSet


class GenreViewSet(BaseModelViewSet):
    def get_queryset(self):
        return genre_repository.get_all()

    def get_serializer_class(self):
        if self.action == "create":
            return GenreCreateSerializer
        return GenreSerializer
