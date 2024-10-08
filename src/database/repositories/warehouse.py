from typing import Optional, Sequence, Tuple, Type

from sqlalchemy import select

from src.common.exceptions.services import ConflictError, NotFoundError
from src.common.dto.warehouse import ProductStock
from src.database.models.warehouse import WarehouseModel
from src.database.models.product import ProductModel
from src.database.repositories.base import BaseRepository


class WarehouseRepository(BaseRepository):
    __slots__ = ()

    @property
    def model(self) -> Type[WarehouseModel]:
        return WarehouseModel

    async def create(
        self, product_id: int, remaining: Optional[int] = 0
    ) -> Optional[WarehouseModel]:
        stock_note = await self._crud.insert(product_id=product_id, remaining=remaining)
        if not stock_note:
            raise ConflictError("Product stock is already exists")
        return stock_note

    async def update(self, product_id: int, remaining: int) -> Optional[WarehouseModel]:
        product = self.model.product_id == product_id
        stock_note = await self._crud.update(
            product, remaining=self.model.remaining + remaining
        )
        if not stock_note:
            raise NotFoundError("Product not found")
        return stock_note

    async def update_many(
        self, products: Sequence[ProductStock]
    ) -> Sequence[Optional[WarehouseModel]]:
        products = [product.model_dump() for product in products]
        return await self._crud.bulk_update_with_summ(
            products, update_field="remaining", key_field="product_id"
        )

    async def get_all(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> Sequence[Tuple[WarehouseModel, ProductModel]]:
        stmt = (
            select(self.model, ProductModel)
            .join(self.model, ProductModel.id == self.model.product_id)
            .offset(offset)
            .limit(limit)
        )
        return (await self._session.execute(stmt)).merge()

    async def delete(self, product_id: int) -> Optional[WarehouseModel]:
        return await self._crud.delete(product_id=product_id)
