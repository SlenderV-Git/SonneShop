from typing import Optional, Type
import uuid

from backend.database.models import AccountModel
from backend.database.repositories.base import BaseRepository


class AccountRepository(BaseRepository):
    __slots__ = ()
    
    @property
    def model(self) -> Type[AccountModel]:
        return AccountModel
    
    async def create(self, user_id : uuid.UUID) -> Optional[AccountModel]:
        return await self._crud.insert(user_id = user_id)
    

    async def get_all(self, user_id: uuid.UUID) -> Optional[AccountModel]:
        condition = self.model.user_id == user_id
        
        return await self._crud.select_many(condition)
    
    async def update(
        self,
        account_id : int,
        amount : int
    ) -> Optional[AccountModel]:
        account = self.model.id == account_id

        return await self._crud.update(account, balance = amount)
    
    async def delete(self, account_id: int) -> Optional[AccountModel]:
        condition = self.model.id == account_id

        return await self._crud.delete(condition)