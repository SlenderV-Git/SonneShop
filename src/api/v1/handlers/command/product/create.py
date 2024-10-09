from sqlalchemy.exc import IntegrityError
from typing import Any
from src.common.exceptions.services import ConflictError
from src.api.v1.handlers.command.base import Command
from src.common.dto.product import CreateProductQuery, Product
from src.services.gateway import ServicesGateway


class ProductCreateCommand(Command[CreateProductQuery, Product]):
    __slots__ = "_gateway"

    def __init__(self, service_gateway: ServicesGateway) -> None:
        self._gateway = service_gateway

    async def execute(self, query: CreateProductQuery, **kwargs: Any) -> Product:
        async with self._gateway:
            try:
                await self._gateway._database.manager.create_transaction()
                product = await self._gateway.product().create(query)
                await self._gateway.warehouse().create(product.id)
                return product
            except IntegrityError:
                raise ConflictError("Product is already exists")
