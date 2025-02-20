__all__ = ["router"]

from uuid import UUID

from fastapi import APIRouter
from starlette import status

from app import schemas
from app.api.dependencies import admin_user, author_service, SQLUnitOfWorkDep, current_user

router = APIRouter(prefix="/author", tags=["Author"])


@router.get("s", response_model=schemas.GetAuthorsResponse, status_code=status.HTTP_200_OK)
async def get_authors(
    _: current_user, service: author_service, uow: SQLUnitOfWorkDep, page: int = 0, per_page: int = 10
):
    return await service.get_authors(page, per_page, uow)


@router.post("", response_model=schemas.CreateAuthorResponse, status_code=status.HTTP_201_CREATED)
async def create_author(
    _: admin_user, request: schemas.CreateAuthorRequest, service: author_service, uow: SQLUnitOfWorkDep
):
    return await service.create_author(request, uow)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(id: UUID, _: admin_user, service: author_service, uow: SQLUnitOfWorkDep):
    await service.delete_author(id, uow)
