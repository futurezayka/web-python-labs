from uuid import UUID

from fastapi import APIRouter
from starlette import status

from app import schemas
from app.api.dependencies import admin_user, genre_service, SQLUnitOfWorkDep, current_user

router = APIRouter(prefix="/genre", tags=["Genre"])
__all__ = ["router"]


@router.get("s", response_model=schemas.GetGenresResponse, status_code=status.HTTP_200_OK)
async def get_genres(_: current_user, service: genre_service, uow: SQLUnitOfWorkDep, page: int = 0, per_page: int = 10):
    return await service.get_genres(page, per_page, uow)


@router.post("", response_model=schemas.CreateGenreResponse, status_code=status.HTTP_201_CREATED)
async def create_genre(
    _: admin_user, request: schemas.CreateGenreRequest, service: genre_service, uow: SQLUnitOfWorkDep
):
    return await service.create_genre(request, uow)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_genre(id: UUID, _: admin_user, service: genre_service, uow: SQLUnitOfWorkDep):
    await service.delete_genre(id, uow)
