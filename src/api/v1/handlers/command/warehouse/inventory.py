from typing import Any
from src.api.v1.handlers.command.base import Command
from src.common.dto.warehouse import ConductInventoryWarehouse, Warehouse
from src.services.gateway import ServicesGateway


class InventoryWarehouseCommand(Command[ConductInventoryWarehouse, Warehouse]):
    __slots__ = "_gateway"

    def __init__(self, service_gateway: ServicesGateway) -> None:
        self._gateway = service_gateway

    async def execute(
        self, query: ConductInventoryWarehouse, **kwargs: Any
    ) -> Warehouse:
        async with self._gateway:
            products = await self._gateway.warehouse().get_all(
                query.limit, query.offset
            )
            return Warehouse(products=products)
