from typing import Any
from src.api.v1.handlers.command.base import Command
from src.common.dto.account import AccountBalanceQuery, AllAccountsBalanceQuery, Balance
from src.services.gateway import ServicesGateway


class GetAccountBalanceCommand(Command[AccountBalanceQuery, Balance]):
    __slots__ = "_gateway"

    def __init__(self, service_gateway: ServicesGateway) -> None:
        self._gateway = service_gateway

    async def execute(self, query: AccountBalanceQuery, **kwargs: Any) -> Balance:
        async with self._gateway:
            return await self._gateway.account().get_balance(
                user_id=query.user_id, account_id=query.id
            )


class GetAllAccountsBalanceCommand(
    Command[
        AllAccountsBalanceQuery,
    ]
):
    __slots__ = "_gateway"

    def __init__(self, service_gateway: ServicesGateway) -> None:
        self._gateway = service_gateway

    async def execute(self, query: AllAccountsBalanceQuery, **kwargs: Any) -> Balance:
        async with self._gateway:
            return await self._gateway.account().get_balance_all(query.user_id)
