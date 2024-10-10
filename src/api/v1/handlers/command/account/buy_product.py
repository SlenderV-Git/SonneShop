from typing import Any
from src.api.v1.handlers.command.base import Command
from src.common.dto.account import Account, BuyProductQuery
from src.services.gateway import ServicesGateway


class BuyProductCommand(Command[BuyProductQuery, Account]):
    __slots__ = "_gateway"

    def __init__(self, service_gateway: ServicesGateway) -> None:
        self._gateway = service_gateway

    async def execute(self, query: BuyProductQuery, **kwargs: Any) -> Account:
        async with self._gateway:
            await self._gateway._database.manager.create_transaction()
            product = await self._gateway.product().get(query.product_id)
            return await self._gateway.account().replenish(
                query.user_id, query.id, -product.price * query.count
            )
