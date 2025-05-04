from pydantic import Field

from app.core.config.base import BaseConfig


class MongoDbConfig(BaseConfig):
    USER: str = Field(..., alias="MONGO_USER")
    PASSWORD: str = Field(..., alias="MONGO_PASSWORD")
    HOST: str = Field(..., alias="MONGO_HOST")
    PORT: str = Field(..., alias="MONGO_PORT")
    DB: str = Field(..., alias="MONGO_DB")

    @property
    def url(self) -> str:
        return f"mongodb://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}"
