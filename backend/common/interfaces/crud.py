from abc import ABC
from typing import Any, Generic, Mapping, Optional, Sequence

from backend.common.types import ModelType


class AbstractCrudRepository(ABC):
    def __init__(self, model: Generic[ModelType]) -> None:
        self.model = model
        
    async def select(self, *args : Any) -> Optional[ModelType]:
        raise NotImplemented
    
    async def select_many(
            self,
            *args : Any, 
            offset : Optional[int] = None, 
            limit : Optional[int] = None
    ) -> Optional[Sequence[ModelType]]:
        raise NotImplemented
    
    async def insert(self, **kwargs : Mapping[str, Any]) -> Optional[ModelType]:
        raise NotImplemented
    
    async def insert_many(self, **kwargs : Sequence[Mapping[str, Any]]) -> Optional[Sequence[ModelType]]:
        raise NotImplemented
    
    async def update(self, **kwargs : Mapping[str, Any]) -> Optional[ModelType]:
        raise NotImplemented
    
    async def update_many(self, **kwargs : Sequence[Mapping[str, Any]]) -> Optional[Sequence[ModelType]]:
        raise NotImplemented
    
    async def delete(self, *args : Any) -> Optional[ModelType]:
        raise NotImplemented