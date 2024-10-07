from typing import Optional, Sequence
from src.common.dto.warehouse import ProductStock, ProductDTO
from src.common.interfaces.gateway import BaseGateway
from src.database.converter import from_model_to_dto, from_many_models_to_list_dto
from src.database.repositories.warehouse import WarehouseRepository


class WarehouseService(BaseGateway):
    __slots__ = "_repository"

    def __init__(self, repository: WarehouseRepository) -> None:
        self._repository = repository

    async def create(self, product_id: int) -> ProductStock:
        return from_model_to_dto(
            await self._repository.create(product_id), ProductStock
        )

    async def update_remaining(self, product_id: int, remaining: int) -> ProductStock:
        return from_model_to_dto(
            await self._repository.update(product_id, remaining), ProductStock
        )

    async def update_many_remaining(self, data: ProductStock) -> Sequence[ProductStock]:
        return await self._repository.update_many(data)

    async def get_all(self, limit: Optional[int] = None, offset: Optional[int] = None):
        product_stock = await self._repository.get_all(limit, offset)
        return from_many_models_to_list_dto(product_stock, ProductDTO)
