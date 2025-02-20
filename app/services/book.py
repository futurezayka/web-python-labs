from uuid import UUID

from app import schemas
from app.schemas import CreateBookRequest, CreateBookResponse
from app.uow.sql import SQLUnitOfWork


class BookService:
    @staticmethod
    async def create_book(request: CreateBookRequest, uow: SQLUnitOfWork) -> CreateBookResponse:
        async with uow:
            await uow.books.create(obj_in=request.model_dump())
        return CreateBookResponse(message="Book created")

    @staticmethod
    async def get_books(uow: SQLUnitOfWork, page: int, per_page: int) -> schemas.GetBooksResponse:
        async with uow:
            return await uow.books.get_multi(page, per_page)

    @staticmethod
    async def delete_book(id: UUID, uow: SQLUnitOfWork) -> None:
        async with uow:
            await uow.books.delete(filters={"id": id})

    @staticmethod
    async def patch_book(id: UUID, request: schemas.UpdateBookRequest, uow: SQLUnitOfWork) -> None:
        async with uow:
            await uow.books.update(filters={"id": id}, updates=request.model_dump(exclude_unset=True))
