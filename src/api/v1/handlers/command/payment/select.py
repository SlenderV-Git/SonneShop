from typing import Any

from src.api.v1.handlers.command.base import Command
from src.common.dto.transaction import (
    SelectTransactionsQuery,
    TransactionWithStatus,
    TransactionsResponse,
)
from src.services.gateway import ServicesGateway


class GetPaymentCommand(Command[SelectTransactionsQuery, TransactionWithStatus]):
    __slots__ = "_gateway"

    def __init__(self, service_gateway: ServicesGateway) -> None:
        self._gateway = service_gateway

    async def execute(
        self, query: SelectTransactionsQuery, **kwargs: Any
    ) -> TransactionsResponse:
        async with self._gateway:
            transactions = await self._gateway.transaction().get_all(
                user_id=query.user_id
            )
            return TransactionsResponse(transactions=transactions)
