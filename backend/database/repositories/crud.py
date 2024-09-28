from typing import Any, Coroutine, Mapping, Sequence, Type

from sqlalchemy import CursorResult, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.common.interfaces.crud import AbstractCrudRepository
from backend.common.types import ModelType


class CrudRepository(AbstractCrudRepository):
    def __init__(self, session: AsyncSession, model: Type[ModelType]) -> None:
        super().__init__(model)
        self._session = session

    async def select(self, *args: Any) -> ModelType | None:

        stmt = select(self.model).where(*args)
        return (await self._session.execute(stmt)).scalars().first()

    async def select_many(
        self, *args: Any, offset: int | None = None, limit: int | None = None
    ) -> Sequence[ModelType] | None:

        stmt = select(self.model).where(*args).offset(offset).limit(limit)
        return (await self._session.execute(stmt)).scalars().all()

    async def insert(self, **kwargs: Mapping[str, Any]) -> ModelType | None:

        stmt = insert(self.model).values(**kwargs).returning(self.model)
        return (await self._session.scalars(stmt, kwargs)).first()

    async def insert_many(
        self, **kwargs: Sequence[Mapping[str, Any]]
    ) -> Sequence[ModelType] | None:

        stmt = insert(self.model).returning(self.model)
        return (await self._session.scalars(stmt, kwargs)).all()

    async def update(self, *args, **kwargs: Mapping[str, Any]) -> ModelType | None:

        stmt = update(self.model).where(*args).values(**kwargs).returning(self.model)
        return (await self._session.execute(stmt)).scalars().first()

    async def update_many(self, data: Sequence[Mapping[str, Any]]) -> CursorResult[Any]:

        return await self._session.execute(update(self.model), data)

    async def delete(self, *args: Any) -> ModelType | None:

        stmt = delete(self.model).where(*args).returning(self.model)
        return (await self._session.execute(stmt)).scalars().first()
