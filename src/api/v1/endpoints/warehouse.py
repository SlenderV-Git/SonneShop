from typing import Annotated, Optional

from fastapi import APIRouter, Depends, status

from src.common.dto.stock_log import AddProductsqQuery
from src.api.v1.handlers.auth.roles import Roles
from src.common.dto import Status, User, Stock
from src.api.v1.handlers.auth.auth import Authorization
from src.api.common.responses import OkResponse
from src.api.common.mediator.mediator import CommandMediator
from src.api.common.providers.stub import Stub
from src.common.dto.warehouse import Warehouse, ConductInventoryWarehouse
from src.api.v1.docs.warehouse import (
    INVENT_DESCRIPTION,
    INVENT_RESPONCE,
    INVENT_SUMMARY,
    OPERATION_DESCRIPTION,
    OPERATION_RESPONCE,
    OPERATION_SUMMARY,
)


warehouse_router = APIRouter(tags=["warehouse"])


@warehouse_router.get(
    "/inventory",
    response_model=Warehouse,
    status_code=status.HTTP_200_OK,
    response_description=INVENT_RESPONCE,
    description=INVENT_DESCRIPTION,
    summary=INVENT_SUMMARY,
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
    "/bulk_update",
    response_model=Status,
    status_code=status.HTTP_200_OK,
    response_description=OPERATION_RESPONCE,
    description=OPERATION_DESCRIPTION,
    summary=OPERATION_SUMMARY,
)
async def update_warehouse_router(
    stock: Stock,
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
    _: Annotated[User, Depends(Authorization(Roles.admin))],
) -> OkResponse[Status]:
    await mediator.send(AddProductsqQuery(operations=stock.operations))
    return OkResponse(Status(ok=True))
