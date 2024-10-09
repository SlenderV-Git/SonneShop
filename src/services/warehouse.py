from typing import Optional, Sequence
from src.common.enum.operation import OperationType
from src.common.dto.warehouse import ProductStock, ProductDTO, ProductStockDB
from src.common.dto.stock_log import StockOperation
from src.common.interfaces.gateway import BaseGateway
from src.common.exceptions import NotFoundException
from src.database.converter import (
    from_model_to_dto,
    from_many_models_to_list_dto,
    from_list_model_to_list_dto,
)
from src.database.repositories.warehouse import WarehouseRepository


class WarehouseService(BaseGateway):
    __slots__ = "_repository"

    def __init__(self, repository: WarehouseRepository) -> None:
        self._repository = repository

    async def create(self, product_id: int) -> ProductStock:
        return from_model_to_dto(
            await self._repository.create(product_id), ProductStockDB
        )

    async def update_remaining(self, product_id: int, remaining: int) -> ProductStock:
        return from_model_to_dto(
            await self._repository.update(product_id, remaining), ProductStockDB
        )

    async def update_many_remaining(
        self, data: Sequence[ProductStock]
    ) -> Sequence[ProductStock]:
        return from_list_model_to_list_dto(
            await self._repository.update_many(data), ProductStockDB
        )

    async def get_all(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> Sequence[ProductDTO]:
        product_stock = await self._repository.get_all(limit, offset)
        return from_many_models_to_list_dto(product_stock, ProductDTO)

    async def delete(self, product_id: int) -> ProductStock:
        product_stock = await self._repository.delete(product_id)
        if not product_stock:
            raise NotFoundException("Product stock not found")
        return product_stock

    async def logs_in_remaining(
        self, operations: Sequence[StockOperation]
    ) -> Sequence[ProductStock]:
        stocks = []
        for operation in operations:
            remaining = (
                operation.quantity
                if not OperationType.outbound == operation.type_operation
                else -operation.quantity
            )
            stocks.append(
                ProductStock(product_id=operation.product_id, remaining=remaining)
            )
        return stocks
