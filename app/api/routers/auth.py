from fastapi import APIRouter
from starlette import status

from app.api.dependencies import SQLUnitOfWorkDep, auth_service
from app.schemas.auth import (
    SignupRequest,
    SignupResponse,
    LoginRequest,
    LoginResponse,
)

__all__ = ["router"]

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", response_model=SignupResponse, status_code=status.HTTP_200_OK)
async def signup(request: SignupRequest, service: auth_service, uow: SQLUnitOfWorkDep):
    return await service.register_user(**request.model_dump(), uow=uow)


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(request: LoginRequest, service: auth_service, uow: SQLUnitOfWorkDep):
    return await service.login(**request.model_dump(), uow=uow)
