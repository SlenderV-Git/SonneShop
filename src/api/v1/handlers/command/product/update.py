from typing import Any
from src.api.v1.handlers.command.base import Command
from src.common.dto.product import UpdateProductQuery, Product, ProductSchema
from src.services.gateway import ServicesGateway


class UpdateProductCommand(Command[UpdateProductQuery, Product]):
    __slots__ = "_gateway"

    def __init__(self, service_gateway: ServicesGateway) -> None:
        self._gateway = service_gateway

    async def execute(self, query: UpdateProductQuery, **kwargs: Any) -> Product:
        async with self._gateway:
            await self._gateway._database.manager.create_transaction()
            return await self._gateway.product().update(
                query.id, ProductSchema(**query.model_dump())
            )
