from typing import Any
from src.api.v1.handlers.command.base import Command
from src.common.dto.product import DeleteProductQuery, Product
from src.services.gateway import ServicesGateway


class ProductDeleteCommand(Command[DeleteProductQuery, Product]):
    __slots__ = "_gateway"

    def __init__(self, service_gateway: ServicesGateway) -> None:
        self._gateway = service_gateway

    async def execute(self, query: DeleteProductQuery, **kwargs: Any) -> Product:
        async with self._gateway:
            await self._gateway._database.manager.create_transaction()
            await self._gateway.warehouse().delete(query.product_id)
            return await self._gateway.product().delete(query.product_id)
