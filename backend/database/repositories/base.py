from abc import abstractmethod
from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession

from backend.common.types import ModelType

from .crud import CrudRepository


class BaseRepository:
    def __init__(self, session : AsyncSession) -> None:
        self._session = session
        self._crud = CrudRepository(self._session, self.model)
        
    @property
    @abstractmethod
    def model(self) -> Type[ModelType]:
        raise NotImplementedError