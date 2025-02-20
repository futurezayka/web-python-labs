import uuid

from sqlalchemy import ForeignKey, UUID, String, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.models.base import Base, UUIDMixin
from app.schemas import Genre
from app.schemas.author import Author


class Book(Base, UUIDMixin):
    __tablename__ = "book"

    author_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("author.id", ondelete="SET NULL"), index=True, nullable=True
    )
    genre_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("genre.id", ondelete="SET NULL"), index=True, nullable=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    total_pages: Mapped[int] = mapped_column(Integer(), nullable=False)
    year: Mapped[int] = mapped_column(Integer(), nullable=False)

    author: Mapped[Author | None] = relationship("Author", foreign_keys=[author_id], lazy="joined")
    genre: Mapped[Genre | None] = relationship("Genre", foreign_keys=[genre_id], lazy="joined")
