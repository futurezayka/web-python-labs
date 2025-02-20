from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.enums.role import Role
from app.models.base import Base, UUIDMixin


class User(Base, UUIDMixin):
    __tablename__ = "user"

    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.user)
