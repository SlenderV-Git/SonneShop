from typing import Any
from src.api.v1.handlers.command.base import Command
from src.common.dto.product import GetProductQuery, Product
from src.services.gateway import ServicesGateway


class GetProductCommand(Command[GetProductQuery, Product]):
    __slots__ = "_gateway"

    def __init__(self, service_gateway: ServicesGateway) -> None:
        self._gateway = service_gateway

    async def execute(self, query: GetProductQuery, **kwargs: Any) -> Product:
        async with self._gateway:
            return await self._gateway.product().get(query.id)
