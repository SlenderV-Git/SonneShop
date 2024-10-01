from typing import Any, overload
from src.common.dto.user import User, UserSchema
from src.common.exceptions.services import ConflictError, NotFoundError
from src.common.interfaces.gateway import BaseGateway
from src.common.interfaces.hasher import AbstractHasher
from src.database.converter import from_model_to_dto
from src.database.repositories.user import UserRepository


class UserService(BaseGateway):
    __slots__ = "_repository"

    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def create(self, data: UserSchema, hasher: AbstractHasher) -> User:
        data.password = hasher.hash_password(data.password)

        user = await self._repository.create(**data.model_dump())

        if not user:
            raise ConflictError(f"User with login {data.login} is already exists")

        return from_model_to_dto(user, User)

    @overload
    async def get_one(self, *, login: str) -> User:
        ...

    @overload
    async def get_one(self, *, user_id: int) -> User:
        ...

    async def get_one(self, **kwargs: Any):
        user = await self._repository.get_one(**kwargs)

        if not user:
            raise NotFoundError(
                f"Searching for a user by parameters {kwargs} did not yield any results"
            )

        return from_model_to_dto(user, User)
