from app.enums.base import BaseStrEnum

__all__ = ["MessageException"]


class MessageException(BaseStrEnum):
    user_not_found = "user_not_found"
    could_not_validate_credentials = "could_not_validate_credentials"
    password_is_not_valid = "password_is_not_valid"
    user_deleted = "user_deleted"
    object_not_found = "object_not_found"
    object_already_exists = "object_already_exists"
    not_authorized = "not_authorized"
    forbidden = "forbidden"
    bad_request = "bad_request"
