from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from core.api.utils.pagination import BasePagination
from core.permissions.admin import IsAdminUser


class BaseModelViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
):
    permission_classes = [IsAuthenticated]
    pagination_class = BasePagination
    http_method_names = ["get", "post", "delete", "patch"]

    def get_permissions(self):
        if self.action in ["create", "destroy", "update"]:
            return [IsAdminUser()]
        return super().get_permissions()

    def get_queryset(self):
        raise NotImplementedError

    def get_serializer_class(self):
        raise NotImplementedError
