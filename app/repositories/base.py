from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import TypeVar, Generic

from sqlalchemy import select, and_, ColumnElement, func, delete, desc, asc, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from app.core.exc import ObjectAlreadyExistsException, ObjectNotFoundException

T = TypeVar("T")
action_map = {
    "eq": "__eq__",
    "ne": "__ne__",
    "lt": "__lt__",
    "le": "__le__",
    "gt": "__gt__",
    "ge": "__ge__",
    "contains": "contains",
    "in": "in_",
    "not_in": "notin_",
    "ilike": "ilike",
    "is_not": "is_not",
}


class AbstractRepositoryMixin(ABC, Generic[T]):
    model: type[T]

    def __init__(self, session: AsyncSession):
        self._session = session

    @abstractmethod
    async def create(self, obj_in: dict[str, any] | T) -> T:
        pass

    @abstractmethod
    async def create_many(self, obj_in: list[dict[str, any]]) -> None:
        pass

    @abstractmethod
    async def get(self, filters: dict[str, any]) -> T | None:
        pass

    @abstractmethod
    async def get_multi_without_pagination(self, order_by: str | None = None, **filters: any) -> Sequence[T]:
        pass

    @abstractmethod
    async def get_multi(
        self, offset: int = 0, limit: int = 10, order_by: str | None = None, **filters: any
    ) -> tuple[Sequence[T], int]:
        pass

    @abstractmethod
    def get_where_clauses(self, filters: dict[str, any]) -> list[T]:
        pass

    @abstractmethod
    async def update(self, filters: dict[str, any], updates: dict[str, any]) -> T | None:
        pass

    @abstractmethod
    async def update_many(self, filters: dict[str, any], updates: dict[str, any]) -> int:
        pass

    @abstractmethod
    async def delete(self, filters: dict[str, any]) -> None:
        pass

    @abstractmethod
    async def delete_many(self, filters: dict[str, any]) -> None:
        pass

    @abstractmethod
    async def count(self, filters: dict[str, any]) -> int:
        pass


class RepositoryMixin(AbstractRepositoryMixin[T]):
    async def create(self, obj_in: dict[str, any]) -> T:
        obj = self.model(**obj_in)
        async with self._session as session:
            try:
                session.add(obj)
                await session.commit()
                await session.refresh(obj)
                return obj
            except IntegrityError:
                raise ObjectAlreadyExistsException(obj_in, self.model.__name__)

    async def create_or_update(
        self, obj_in: dict[str, any], conflict_columns: list[str], update_columns: list[str]
    ) -> None:
        statement = pg_insert(self.model).values(obj_in)
        update_dict = {col: getattr(statement.excluded, col) for col in update_columns if col in obj_in}
        statement = statement.on_conflict_do_update(index_elements=conflict_columns, set_=update_dict)
        async with self._session as session:
            await session.execute(statement)
            await session.commit()

    async def create_many(self, obj_in: list[dict[str, any]]) -> None:
        try:
            statement = pg_insert(self.model).values(obj_in)
            statement = statement.on_conflict_do_nothing()
            await self._session.execute(statement)
        except IntegrityError:
            raise ObjectAlreadyExistsException(obj_in, self.model.__name__)

    async def create_many_or_update(
        self, obj_in: list[dict[str, any]], conflict_columns: list[str], update_columns: list[str]
    ) -> None:
        statement = pg_insert(self.model).values(obj_in)
        update_dict = {col: getattr(statement.excluded, col) for col in update_columns}
        statement = statement.on_conflict_do_update(index_elements=conflict_columns, set_=update_dict)
        await self._session.execute(statement)
        await self._session.commit()

    async def get(self, filters: dict[str, any]) -> T | None:
        async with self._session as session:
            query = select(self.model).where(and_(*[getattr(self.model, k) == v for k, v in filters.items()]))
            result = await session.execute(query)
            obj = result.scalars().first()
            return obj

    async def get_multi(
        self, offset: int = 0, limit: int = 10, order_by: str | None = None, **filters: any
    ) -> tuple[Sequence[T], int]:
        statement = (
            select(self.model, func.count().over().label("total_count"))
            .where(*self.get_where_clauses(filters))
            .offset(offset)
            .limit(limit)
        )
        if order_by:
            if order_by.startswith("-"):
                statement = statement.order_by(desc(getattr(self.model, order_by[1:])).nulls_last())
            else:
                statement = statement.order_by(asc(getattr(self.model, order_by)))

        async with self._session as session:
            result = await session.execute(statement)
            rows = result.all()

        if rows:
            objs = [row[0] for row in rows]
            total_count = rows[0][1]
        else:
            objs = []
            total_count = 0

        return objs, total_count

    async def get_multi_without_pagination(self, order_by: str | None = None, **filters: any) -> Sequence[T]:
        statement = select(self.model).where(*self.get_where_clauses(filters))
        if order_by:
            if order_by.startswith("-"):
                statement = statement.order_by(desc(getattr(self.model, order_by[1:])).nulls_last())
            else:
                statement = statement.order_by(asc(getattr(self.model, order_by)))

        async with self._session as session:
            result = await session.execute(statement)
            objs = result.scalars().all()

        return objs

    def get_where_clauses(self, filters: dict[str, any]) -> list[ColumnElement]:
        clauses: list[ColumnElement] = []
        for key, value in filters.items():
            if "__" not in key:
                key = f"{key}__eq"
            column_name, action_name = key.split("__")
            column: InstrumentedAttribute = getattr(self.model, column_name)
            if column is None:
                raise Exception(f"Column {column_name} not found in {self.model.__name__}")
            action: str | None = action_map.get(action_name, None)
            if action is None:
                raise Exception(f"Action {action_name} not found in action_map")
            clause: ColumnElement = getattr(column, action)(value)
            clauses.append(clause)
        return clauses

    async def update(self, filters: dict[str, any], updates: dict[str, any]) -> T:
        async with self._session as session:
            query = select(self.model).where(and_(*[getattr(self.model, k) == v for k, v in filters.items()]))
            result = await session.execute(query)
            obj = result.scalars().first()
            if not obj:
                raise ObjectNotFoundException(filters, self.model.__name__)

            for key, value in updates.items():
                setattr(obj, key, value)

            try:
                await session.commit()
                await session.refresh(obj)
            except IntegrityError:
                raise ObjectAlreadyExistsException(updates, self.model.__name__)

            return obj

    async def update_many(self, filters: dict[str, any], updates: dict[str, any]) -> int:
        async with self._session as session:
            stmt = update(self.model).where(and_(*self.get_where_clauses(filters))).values(**updates)

            result = await session.execute(stmt)

            await session.commit()

            return result.rowcount or 0

    async def delete(self, filters: dict[str, any]) -> None:
        async with self._session as session:
            query = select(self.model).where(and_(*[getattr(self.model, k) == v for k, v in filters.items()]))
            result = await session.execute(query)
            obj = result.scalars().first()
            if not obj:
                raise ObjectNotFoundException(filters, self.model.__name__)

            await session.delete(obj)
            await session.commit()

    async def delete_many(self, filters: dict[str, any]) -> None:
        query = delete(self.model).where(and_(*self.get_where_clauses(filters)))
        await self._session.execute(query)
        await self._session.commit()

    async def upsert(self, obj_in: dict[str, any], index_columns: list[str]) -> None:
        """
        Insert or update database object based on index columns.

        Args:
           obj_in: Dictionary containing object attributes and their values
           index_columns: List of column names that form the unique index
        """

        update_dict = {k: v for k, v in obj_in.items() if k not in index_columns}

        async with self._session as session:
            statement = (
                pg_insert(self.model)
                .values(**obj_in)
                .on_conflict_do_update(index_elements=index_columns, set_=update_dict)
            )
            await session.execute(statement)
            await session.commit()

    async def count(self, filters: dict[str, any]) -> int:
        statement = select(func.count()).where(and_(*self.get_where_clauses(filters)))
        async with self._session as session:
            result = await session.execute(statement)
            count = result.scalar()
        return count
