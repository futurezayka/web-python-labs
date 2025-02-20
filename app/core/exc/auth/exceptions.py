from app.core.exc.base.exceptions import (
    ObjectNotFoundException,
    ObjectAlreadyExistsException,
    NotAuthorizedException,
    BadRequestException,
)
from app.enums import MessageException

__all__ = [
    "UserAlreadyExistsException",
    "UserNotFoundException",
    "InvalidCredentialsException",
    "UserDeletedException",
    "PasswordNotValidException",
]


class UserAlreadyExistsException(ObjectAlreadyExistsException):
    def __init__(self, email: str) -> None:
        super().__init__(id_=email, model_name="User")


class UserNotFoundException(ObjectNotFoundException):
    def __init__(self, id_: str) -> None:
        super().__init__(id_=id_, model_name="User")


class InvalidCredentialsException(NotAuthorizedException):
    def __init__(self) -> None:
        super().__init__(MessageException.could_not_validate_credentials)


class UserDeletedException(ObjectNotFoundException):
    def __init__(self, id_: str) -> None:
        super().__init__(id_=id_, model_name="User", message=MessageException.user_deleted)


class PasswordNotValidException(BadRequestException):
    def __init__(self) -> None:
        super().__init__(MessageException.password_is_not_valid)
