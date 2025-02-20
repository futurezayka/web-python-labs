from app import schemas
from app.core.exc import ForbiddenException


class PermissionManager:
    @staticmethod
    def ensure_admin(user: schemas.User) -> None:
        if not user.role == "admin":
            raise ForbiddenException


permission_manager = PermissionManager()
