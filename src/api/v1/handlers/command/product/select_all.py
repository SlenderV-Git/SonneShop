from typing import Any
from src.api.v1.handlers.command.base import Command
from src.common.dto.product import GetAllProductsQuery, Product, Products
from src.services.gateway import ServicesGateway


class GetAllProductsCommand(Command[GetAllProductsQuery, Product]):
    __slots__ = "_gateway"

    def __init__(self, service_gateway: ServicesGateway) -> None:
        self._gateway = service_gateway

    async def execute(self, query: GetAllProductsQuery, **kwargs: Any) -> Product:
        async with self._gateway:
            products = await self._gateway.product().get_all(
                limit=query.limit, offset=query.offset
            )
            return Products(products=products)
