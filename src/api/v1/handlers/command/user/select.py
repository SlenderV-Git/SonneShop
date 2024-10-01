from typing import Any
from src.api.v1.handlers.command.base import Command
from src.common.dto.user import SelectUserQuery, User
from src.common.exceptions.services import AttributeNotSpecifiedError
from src.services.gateway import ServicesGateway


class UserSelectCommand(Command[SelectUserQuery, User]):
    __slots__ = "_gateway"

    def __init__(self, service_gateway: ServicesGateway) -> None:
        self._gateway = service_gateway

    async def execute(self, query: SelectUserQuery, **kwargs: Any) -> User:
        async with self._gateway:
            if not query.id and not query.login:
                raise AttributeNotSpecifiedError("Specify user id or login for search")
            elif query.id:
                return await self._gateway.user().get_one(user_id=query.id)
            elif query.login:
                return await self._gateway.user().get_one(login=query.login)
