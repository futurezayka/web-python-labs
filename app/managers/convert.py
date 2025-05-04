from app import schemas, models


class ConvertManager:
    @staticmethod
    def convert_user(user: models.User | dict) -> schemas.User:
        if user:
            return (
                schemas.User(**user, id=user.get("_id"))
                if isinstance(user, dict)
                else schemas.User(
                    id=user.id,
                    email=user.email,
                    password_hash=user.password_hash,
                    role=user.role,
                )
            )

    @staticmethod
    def convert_book(book: models.Book | dict) -> schemas.Book:
        if book:
            return (
                schemas.Book(**book, id=book.get("_id"))
                if isinstance(book, dict)
                else schemas.Book(
                    id=book.id,
                    title=book.title,
                    author=schemas.Author(name=book.author.name, pseudonym=book.author.pseudonym),
                    genre=schemas.Genre(name=book.genre.name),
                    year=book.year,
                    total_pages=book.total_pages,
                )
            )

    @staticmethod
    def convert_genre(genre: models.Genre | dict) -> schemas.Genre:
        if genre:
            return (
                schemas.Genre(**genre, id=genre.get("_id"))
                if isinstance(genre, dict)
                else schemas.Genre(
                    id=genre.id,
                    name=genre.name,
                )
            )

    @staticmethod
    def convert_author(author: models.Author | dict) -> schemas.Author:
        if author:
            return (
                schemas.Author(**author, id=author.get("_id"))
                if isinstance(author, dict)
                else schemas.Author(
                    id=author.id,
                    name=author.name,
                    pseudonym=author.pseudonym,
                )
            )
