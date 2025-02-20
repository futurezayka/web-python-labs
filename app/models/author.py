from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin


class Author(Base, UUIDMixin):
    __tablename__ = "author"

    name: Mapped[str] = mapped_column(String(255))
    pseudonym: Mapped[str] = mapped_column(String(255))
