from pydantic import EmailStr, BaseModel


class AccessTokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class SignupRequest(BaseModel):
    email: EmailStr
    password: str


class SignupResponse(AccessTokenResponse): ...


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(AccessTokenResponse): ...
