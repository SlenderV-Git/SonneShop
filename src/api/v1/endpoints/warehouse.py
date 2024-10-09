from typing import Annotated, Optional

from fastapi import APIRouter, Depends, status

from src.api.v1.handlers.auth.roles import Roles
from src.common.dto import Status, User, Stock, ConductMassUpdateStockpile
from src.api.v1.handlers.auth.auth import Authorization
from src.api.common.responses import OkResponse
from src.api.common.mediator.mediator import CommandMediator
from src.api.common.providers.stub import Stub
from src.common.dto.warehouse import Warehouse, ConductInventoryWarehouse


warehouse_router = APIRouter(tags=["warehouse"])


@warehouse_router.get(
    "/inventory", response_model=Warehouse, status_code=status.HTTP_200_OK
)
async def inventory_warehouse_router(
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
    _: Annotated[User, Depends(Authorization(Roles.admin))],
    limit: Optional[int | None] = None,
    offset: Optional[int | None] = None,
) -> OkResponse[Warehouse]:
    warehouse = await mediator.send(
        ConductInventoryWarehouse(limit=limit, offset=offset)
    )
    return OkResponse(warehouse)


@warehouse_router.post(
    "/bulk_update", response_model=Status, status_code=status.HTTP_200_OK
)
async def update_warehouse_router(
    stock: Stock,
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
    _: Annotated[User, Depends(Authorization(Roles.admin))],
) -> OkResponse[Status]:
    await mediator.send(ConductMassUpdateStockpile(products=stock.operations))
    return OkResponse(Status(ok=True))
