from typing import Any
from src.api.v1.handlers.command.base import Command
from src.common.dto.stock_log import AddProductsqQuery, Stock
from src.services.gateway import ServicesGateway


class AddProductsCommand(Command[AddProductsqQuery, Stock]):
    __slots__ = "_gateway"

    def __init__(self, service_gateway: ServicesGateway) -> None:
        self._gateway = service_gateway

    async def execute(self, query: AddProductsqQuery, **kwargs: Any) -> Stock:
        async with self._gateway:
            await self._gateway._database.manager.create_transaction()
            remainings = await self._gateway.warehouse().logs_in_remaining(
                query.operations
            )
            await self._gateway.warehouse().update_many_remaining(remainings)
            operations = await self._gateway.stock_log().create_many(query.operations)

            return Stock(operations=operations)
