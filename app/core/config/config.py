from pydantic import Field

from app.core.config.auth import AuthConfig
from app.core.config.base import BaseConfig
from app.core.config.db import DataBaseConfig
from app.core.config.mongo import MongoDbConfig

__all__ = ["Settings", "settings"]


class Settings(BaseConfig):
    SERVER_HOST: str = Field(..., alias="SERVER_HOST")
    SERVER_PORT: int = Field(..., alias="SERVER_PORT")
    RELOAD: bool = Field(False, alias="RELOAD")

    db: DataBaseConfig = DataBaseConfig()
    auth: AuthConfig = AuthConfig()
    mongo: MongoDbConfig = MongoDbConfig()


settings = Settings()
