from typing import Optional, Sequence
from src.common.dto.stock_log import StockOperation
from src.common.interfaces.gateway import BaseGateway
from src.database.converter import from_model_to_dto, from_list_model_to_list_dto
from src.database.repositories.stock_log import StockLogRepository


class StockLogService(BaseGateway):
    __slots__ = "_repository"

    def __init__(self, repository: StockLogRepository) -> None:
        self._repository = repository

    async def create(self, operation: StockOperation) -> StockOperation:
        return from_model_to_dto(
            await self._repository.create(operation), StockOperation
        )

    async def get_product_logs(
        self, product_id: int, offset: Optional[int] = None, limit: Optional[int] = None
    ) -> Sequence[StockOperation]:
        return from_list_model_to_list_dto(
            await self._repository.get_product_logs(product_id, offset, limit),
            StockOperation,
        )
