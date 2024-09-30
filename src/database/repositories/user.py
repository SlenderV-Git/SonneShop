from typing import Optional, Type, overload
import uuid

from src.common.dto.user import UserSchema
from src.common.exceptions.database import InvalidParamsError
from src.database.models.user import UserModel
from src.database.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    __slots__ = ()

    @property
    def model(self) -> Type[UserModel]:
        return UserModel

    async def create(self, **data: UserSchema) -> Optional[UserModel]:
        return await self._crud.insert(**data)

    @overload
    async def get_one(self, *, user_id: uuid.UUID) -> Optional[UserModel]:
        ...

    @overload
    async def get_one(self, *, login: str) -> Optional[UserModel]:
        ...

    async def get_one(
        self, *, user_id: Optional[int] = None, login: Optional[int] = None
    ) -> Optional[UserModel]:
        if not any([user_id, login]):
            raise InvalidParamsError("at least one identifier must be provided")

        condition = self.model.id == user_id if user_id else self.model.login == login

        return await self._crud.select(condition)

    async def update(self, user_id: int, **data: UserSchema) -> Optional[UserModel]:
        condition = self.model.id == user_id

        return await self._crud.update(condition, **data)

    async def delete(self, user_id: int) -> Optional[UserModel]:
        clause = self.model.id == user_id

        return await self._crud.delete(clause)
