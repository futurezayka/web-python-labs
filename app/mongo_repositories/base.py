from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Any
from motor.motor_asyncio import AsyncIOMotorDatabase

T = TypeVar("T")

class AbstractRepositoryMixin(ABC, Generic[T]):
    collection_name: str

    def __init__(self, db: AsyncIOMotorDatabase):
        self._db = db
        self._collection = db[self.collection_name]

    @abstractmethod
    async def create(self, obj_in: dict[str, Any]) -> Any:
        pass

    @abstractmethod
    async def get(self, filters: dict[str, Any]) -> Any:
        pass

    @abstractmethod
    async def get_multi(self, offset: int = 0, limit: int = 10, **filters: Any) -> list[Any]:
        pass

    @abstractmethod
    async def update(self, filters: dict[str, Any], updates: dict[str, Any]) -> Any:
        pass

    @abstractmethod
    async def delete(self, filters: dict[str, Any]) -> None:
        pass

class RepositoryMixin(AbstractRepositoryMixin[T]):
    async def create(self, obj_in: dict[str, Any]) -> Any:
        result = await self._collection.insert_one(obj_in)
        return await self._collection.find_one({"_id": result.inserted_id})

    async def get(self, filters: dict[str, Any]) -> Any:
        return await self._collection.find_one(filters)

    async def get_multi(self, offset: int = 0, limit: int = 10, **filters: Any) -> list[Any]:
        cursor = self._collection.find(filters).skip(offset).limit(limit)
        return await cursor.to_list(length=limit)

    async def update(self, filters: dict[str, Any], updates: dict[str, Any]) -> Any:
        await self._collection.update_one(filters, {"$set": updates})
        return await self.get(filters)

    async def delete(self, filters: dict[str, Any]) -> None:
        await self._collection.delete_one(filters)
