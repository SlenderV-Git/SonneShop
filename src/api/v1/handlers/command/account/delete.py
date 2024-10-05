from typing import Any
from src.api.v1.handlers.command.base import Command
from src.common.dto.account import DeleteAccountQuery, Account
from src.services.gateway import ServicesGateway


class DeleteAccountCommand(Command[DeleteAccountQuery, Account]):
    __slots__ = "_gateway"

    def __init__(self, service_gateway: ServicesGateway) -> None:
        self._gateway = service_gateway

    async def execute(self, query: DeleteAccountQuery, **kwargs: Any) -> Account:
        async with self._gateway:
            await self._gateway._database.manager.create_transaction()
            return await self._gateway.account().delete_account(
                user_id=query.user_id, account_id=query.id
            )
