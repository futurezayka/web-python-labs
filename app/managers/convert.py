from app import schemas, models


class ConvertManager:
    @staticmethod
    def convert_user(user: models.User) -> schemas.User:
        if user:
            return schemas.User(
                id=user.id,
                email=user.email,
                password_hash=user.password_hash,
                role=user.role,
            )

    @staticmethod
    def convert_book(book: models.Book) -> schemas.Book:
        if book:
            return schemas.Book(
                id=book.id,
                title=book.title,
                author=schemas.Author(name=book.author.name, pseudonym=book.author.pseudonym),
                genre=schemas.Genre(name=book.genre.name),
                year=book.year,
                total_pages=book.total_pages,
            )

    @staticmethod
    def convert_genre(genre: models.Genre) -> schemas.Genre:
        if genre:
            return schemas.Genre(
                name=genre.name,
            )

    @staticmethod
    def convert_author(author: models.Author) -> schemas.Author:
        if author:
            return schemas.Author(
                name=author.name,
                pseudonym=author.pseudonym,
            )
