from typing import Optional, Sequence, Type
import uuid

from backend.common.dto.product import ProductSchema
from backend.database.models.product import ProductModel
from backend.database.repositories.base import BaseRepository


class ProductRepostory(BaseRepository):
    __slots__ = ()
    
    @property
    def model(self) -> Type[ProductModel]:
        return ProductModel
    
    async def create(self, **product : ProductSchema) -> Optional[ProductModel]:
        return await self._crud.insert(**product)
    

    async def get_one(self, product_id: uuid.UUID) -> Optional[ProductModel]:
        condition = self.model.id == product_id
        return await self._crud.select(condition)
    
    async def get_all(
        self, 
        offset : Optional[int] = None,
        limit : Optional[int] = None
    ) -> Optional[Sequence[ProductModel]]:
        return await self._crud.select_many(offset=offset, limit=limit)
    
    
    async def update(
        self,
        product_id : int,
        **product : ProductSchema
    ) -> Optional[ProductModel]:
        condition = self.model.id == product_id

        return await self._crud.update(condition, **product)
    
    async def delete(self, product_id: int) -> Optional[ProductModel]:
        condition = self.model.id == product_id

        return await self._crud.delete(condition)