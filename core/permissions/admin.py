from rest_framework.permissions import BasePermission

from core.enums.role import Role


class HasRole(BasePermission):
    def __init__(self, role: str):
        self.role = role

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == self.role


class IsAdminUser(HasRole):
    def __init__(self):
        super().__init__(Role.ADMIN)
