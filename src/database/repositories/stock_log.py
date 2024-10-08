from typing import Optional, Sequence, Type

from src.common.dto.stock_log import StockOperation
from src.database.models.stock_log import StockLogModel
from src.database.repositories.base import BaseRepository


class StockLogRepository(BaseRepository):
    __slots__ = ()

    @property
    def model(self) -> Type[StockLogModel]:
        return StockLogModel

    async def create(self, log: StockOperation) -> StockLogModel:
        return await self._crud.insert(**log.model_dump())

    async def create_many(
        self, logs: Sequence[StockOperation]
    ) -> Sequence[StockLogModel]:
        return await self._crud.insert_many(logs)

    async def get_product_logs(
        self, product_id: int, offset: Optional[int] = None, limit: Optional[int] = None
    ) -> Sequence[StockLogModel]:
        condition = self.model.product_id == product_id
        return await self._crud.select_many(condition, limit=limit, offset=offset)
