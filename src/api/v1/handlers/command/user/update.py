from typing import Any, Coroutine
from src.api.v1.handlers.command.base import Command
from src.common.dto.user import UpdateUserQuery, User
from src.services.gateway import ServicesGateway


class UserUpdateCommand(Command[UpdateUserQuery, User]):
    __slots__ = "_gateway"

    def __init__(self, service_gateway: ServicesGateway) -> None:
        self._gateway = service_gateway

    async def execute(
        self, query: UpdateUserQuery, **kwargs: Any
    ) -> Coroutine[Any, Any, User]:
        async with self._gateway:
            await self._gateway._database.manager.create_transaction()

            return await self._gateway.user().update(query.id, query, **kwargs)
