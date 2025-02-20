from uuid import UUID

from fastapi import APIRouter
from starlette import status

from app import schemas
from app.api.dependencies import current_user, admin_user, SQLUnitOfWorkDep, book_service

router = APIRouter(prefix="/book", tags=["Book"])
__all__ = ["router"]


@router.get("s", response_model=schemas.GetBooksResponse, status_code=status.HTTP_200_OK)
async def get_books(
    _: current_user,
    service: book_service,
    uow: SQLUnitOfWorkDep,
    page: int = 0,
    per_page: int = 10,
):
    return await service.get_books(uow, page, per_page)


@router.post("", response_model=schemas.CreateBookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(
    _: admin_user,
    request: schemas.CreateBookRequest,
    uow: SQLUnitOfWorkDep,
    service: book_service,
):
    return await service.create_book(request, uow)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(id: UUID, _: admin_user, uow: SQLUnitOfWorkDep, service: book_service):
    await service.delete_book(id, uow)


@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def patch_book(
    id: UUID, request: schemas.UpdateBookRequest, _: admin_user, uow: SQLUnitOfWorkDep, service: book_service
):
    await service.patch_book(id, request, uow)
