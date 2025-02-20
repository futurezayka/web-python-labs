from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import ExpiredSignatureError

from app import schemas
from app.core.exc.auth import UserAlreadyExistsException
from app.core.exc.auth.exceptions import PasswordNotValidException, UserNotFoundException, InvalidCredentialsException
from app.managers.hash import hash_manager
from app.managers.permission import permission_manager
from app.managers.token import jwt_token_manager
from app.schemas.auth import SignupResponse, LoginResponse
from app.uow.sql import SQLUnitOfWork


class AuthService:
    async def register_user(self, email: str, password: str, uow: SQLUnitOfWork) -> SignupResponse:
        return await self._register(email, password, uow)

    async def _register(self, email: str, password: str, uow: SQLUnitOfWork) -> SignupResponse:
        async with uow:
            if await uow.users.get(filters={"email": email}):
                raise UserAlreadyExistsException

        async with uow:
            await uow.users.create({"email": email, "password_hash": hash_manager.get_hash(password)})

        return SignupResponse(
            access_token=self.create_access_token(email),
            refresh_token=self.create_refresh_token(email),
        )

    async def login(self, email: str, password: str, uow: SQLUnitOfWork) -> LoginResponse:
        return await self._login(email, password, uow)

    async def _login(self, email: str, password: str, uow: SQLUnitOfWork) -> LoginResponse:
        async with uow:
            user = await uow.users.get(filters={"email": email})

        if not user:
            raise UserNotFoundException(email)

        if not hash_manager.verify_hash(password, user.password_hash):
            raise PasswordNotValidException

        return LoginResponse(
            access_token=self.create_access_token(email),
            refresh_token=self.create_refresh_token(email),
        )

    @staticmethod
    async def validate_jwt_token(token) -> schemas.User:
        try:
            payload = jwt_token_manager.decode_token(token.credentials)
        except ExpiredSignatureError:
            raise InvalidCredentialsException
        email = payload.get("sub")

        if email is None:
            raise InvalidCredentialsException

        async with SQLUnitOfWork() as uow:
            user = await uow.users.get(filters={"email": email})

        if user is None:
            raise InvalidCredentialsException

        return user

    @staticmethod
    def create_access_token(email: str) -> str:
        data = {"sub": email, "type": "access"}
        return jwt_token_manager.create_access_token(data)

    @staticmethod
    def create_refresh_token(email: str) -> str:
        data = {"sub": email, "type": "refresh"}
        return jwt_token_manager.create_refresh_token(data)

    @staticmethod
    async def get_current_user(token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]) -> schemas.User:
        return await AuthService.validate_jwt_token(token)

    @staticmethod
    async def get_admin_user(token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]) -> schemas.User:
        user = await AuthService.get_current_user(token)
        if permission_manager.ensure_admin(user):
            return user
