from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin


class Genre(Base, UUIDMixin):
    __tablename__ = "genre"

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
