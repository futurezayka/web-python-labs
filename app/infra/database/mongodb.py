import functools

from bson import CodecOptions, UuidRepresentation
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core import settings

__all__ = ["get_mongo_client", "get_mongo_database"]


@functools.lru_cache
def get_mongo_client() -> AsyncIOMotorClient:
    return AsyncIOMotorClient(
        settings.mongo.url,
    )


@functools.lru_cache
def get_mongo_database() -> AsyncIOMotorDatabase:
    client = get_mongo_client()
    return client.get_database(
        settings.mongo.DB, codec_options=CodecOptions(uuid_representation=UuidRepresentation.PYTHON_LEGACY)
    )
