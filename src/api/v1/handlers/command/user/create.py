from sqlalchemy.exc import IntegrityError
from typing import Any
from src.common.exceptions.services import ConflictError
from src.api.v1.handlers.command.base import Command
from src.common.dto.user import UserSchema, UserResponse
from src.services.gateway import ServicesGateway


class UserCreateCommand(Command[UserSchema, UserResponse]):
    __slots__ = "_gateway"

    def __init__(self, service_gateway: ServicesGateway) -> None:
        self._gateway = service_gateway

    async def execute(self, query: UserSchema, **kwargs: Any) -> UserResponse:
        async with self._gateway:
            try:
                await self._gateway._database.manager.create_transaction()

                return await self._gateway.user().create(query, **kwargs)
            except IntegrityError:
                raise ConflictError("User with this login or mail already exists")
