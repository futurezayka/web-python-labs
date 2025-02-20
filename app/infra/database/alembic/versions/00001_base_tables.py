"""base tables

Revision ID: 00001
Revises:
Create Date: 2025-02-20 20:19:14.123739

"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "00001"
down_revision: str | None = None
branch_labels: Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "author",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("pseudonym", sa.String(length=255), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_author_id"), "author", ["id"], unique=False)
    op.create_table(
        "genre",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_genre_id"), "genre", ["id"], unique=False)
    op.create_index(op.f("ix_genre_name"), "genre", ["name"], unique=True)
    op.create_table(
        "user",
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", sa.Enum("user", "admin", name="role"), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)
    op.create_index(op.f("ix_user_id"), "user", ["id"], unique=False)
    op.create_table(
        "book",
        sa.Column("author_id", sa.UUID(), nullable=True),
        sa.Column("genre_id", sa.UUID(), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("total_pages", sa.Integer(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["author_id"], ["author.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["genre_id"], ["genre.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_book_author_id"), "book", ["author_id"], unique=False)
    op.create_index(op.f("ix_book_genre_id"), "book", ["genre_id"], unique=False)
    op.create_index(op.f("ix_book_id"), "book", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_book_id"), table_name="book")
    op.drop_index(op.f("ix_book_genre_id"), table_name="book")
    op.drop_index(op.f("ix_book_author_id"), table_name="book")
    op.drop_table("book")
    op.drop_index(op.f("ix_user_id"), table_name="user")
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_table("user")
    op.drop_index(op.f("ix_genre_name"), table_name="genre")
    op.drop_index(op.f("ix_genre_id"), table_name="genre")
    op.drop_table("genre")
    op.drop_index(op.f("ix_author_id"), table_name="author")
    op.drop_table("author")
