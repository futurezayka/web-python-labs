from pydantic import Field

from app.core.config.base import BaseConfig
from app.core.config.db import DataBaseConfig

__all__ = ["Settings", "settings"]


class Settings(BaseConfig):
    SERVER_HOST: str = Field(..., alias="SERVER_HOST")
    SERVER_PORT: int = Field(..., alias="SERVER_PORT")
    RELOAD: bool = Field(False, alias="RELOAD")

    db: DataBaseConfig = DataBaseConfig()


settings = Settings()
