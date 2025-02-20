from app.enums.role import Role
from app.schemas.base import IdBase

__all__ = ["User"]


class User(IdBase):
    email: str
    password_hash: str
    role: Role
