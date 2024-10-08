from collections import defaultdict
from typing import Any, Mapping, Optional, Sequence, Type

from sqlalchemy import CursorResult, case, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.interfaces.crud import AbstractCrudRepository
from src.common.types import ModelType


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
        self, kwargs: Sequence[Mapping[str, Any]]
    ) -> Sequence[ModelType] | None:
        stmt = insert(self.model).returning(self.model)
        return (await self._session.scalars(stmt, kwargs)).all()

    async def update(self, *args, **kwargs: Mapping[str, Any]) -> ModelType | None:
        stmt = update(self.model).where(*args).values(**kwargs).returning(self.model)
        return (await self._session.execute(stmt)).scalars().first()

    async def update_many(self, data: Sequence[Mapping[str, Any]]) -> CursorResult[Any]:
        return await self._session.execute(update(self.model), data)

    async def bulk_update_with_summ(
        self,
        data: Sequence[Mapping[str, Any]],
        update_field: str,
        key_field: Optional[str] = "id",
    ) -> CursorResult[Any]:

        grouped_data = defaultdict(lambda: 0)
        for record in data:
            grouped_data[record[key_field]] += record[update_field]

        stmt = (
            update(self.model)
            .where(getattr(self.model, key_field).in_(grouped_data.keys()))
            .values(
                **{
                    update_field: case(
                        {
                            key: getattr(self.model, update_field) + value
                            for key, value in grouped_data.items()
                        },
                        value=getattr(self.model, key_field),
                    )
                }
            )
        )
        return await self._session.execute(stmt)

    async def delete(self, *args: Any) -> ModelType | None:
        stmt = delete(self.model).where(*args).returning(self.model)
        return (await self._session.execute(stmt)).scalars().first()
