from typing import Optional, Type, Sequence
import uuid

from src.database.models import AccountModel
from src.database.repositories.base import BaseRepository


class AccountRepository(BaseRepository):
    __slots__ = ()

    @property
    def model(self) -> Type[AccountModel]:
        return AccountModel

    async def create(self, user_id: uuid.UUID) -> Optional[AccountModel]:
        return await self._crud.insert(user_id=user_id)

    async def get_one(
        self, user_id: uuid.UUID, account_id: int
    ) -> Optional[AccountModel]:
        user = self.model.user_id == user_id
        account = self.model.id == account_id
        return await self._crud.select(account, user)

    async def get_all(self, user_id: uuid.UUID) -> Optional[Sequence[AccountModel]]:
        condition = self.model.user_id == user_id
        return await self._crud.select_many(condition)

    async def update(
        self, user_id: int, account_id: int, amount: int
    ) -> Optional[AccountModel]:
        account = self.model.id == account_id
        user = self.model.user_id == user_id
        return await self._crud.update(
            account, user, balance=self.model.balance + amount
        )

    async def delete(self, user_id: int, account_id: int) -> Optional[AccountModel]:
        condition = self.model.id == account_id
        user = self.model.user_id == user_id
        return await self._crud.delete(condition, user)
