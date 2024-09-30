from abc import ABC
from typing import Any, Generic, Mapping, Optional, Sequence

from src.common.types import ModelType


class AbstractCrudRepository(ABC):
    def __init__(self, model: Generic[ModelType]) -> None:
        self.model = model

    async def select(self, *args: Any) -> Optional[ModelType]:
        raise NotImplementedError

    async def select_many(
        self, *args: Any, offset: Optional[int] = None, limit: Optional[int] = None
    ) -> Optional[Sequence[ModelType]]:
        raise NotImplementedError

    async def insert(self, **kwargs: Mapping[str, Any]) -> Optional[ModelType]:
        raise NotImplementedError

    async def insert_many(
        self, **kwargs: Sequence[Mapping[str, Any]]
    ) -> Optional[Sequence[ModelType]]:
        raise NotImplementedError

    async def update(self, **kwargs: Mapping[str, Any]) -> Optional[ModelType]:
        raise NotImplementedError

    async def update_many(
        self, **kwargs: Sequence[Mapping[str, Any]]
    ) -> Optional[Sequence[ModelType]]:
        raise NotImplementedError

    async def delete(self, *args: Any) -> Optional[ModelType]:
        raise NotImplementedError
