from typing import Optional, Sequence, Type


from src.common.dto.transaction import Transaction
from src.database.models.transaction import TransactionModel
from src.database.repositories.base import BaseRepository


class TransactionRepostory(BaseRepository):
    __slots__ = ()

    @property
    def model(self) -> Type[TransactionModel]:
        return TransactionModel

    async def create(self, user_id: int, data: Transaction) -> TransactionModel:
        return await self._crud.insert(user_id=user_id, **data.model_dump())

    async def update(self, transaction_id: int, approved: bool) -> TransactionModel:
        condition = self.model.id == transaction_id
        return await self._crud.update(condition, approved=approved)

    async def get_all(
        self, user_id: int, offset: int = None, limit: int = None
    ) -> Sequence[Optional[TransactionModel]]:
        condition = self.model.user_id == user_id
        return await self._crud.select_many(condition, offset=offset, limit=limit)
