from typing import Annotated, Optional

from fastapi import APIRouter, Depends, status

from src.api.v1.handlers.auth.roles import Roles
from src.common.dto.user import User
from src.api.v1.handlers.auth.auth import Authorization
from src.api.common.responses import OkResponse
from src.api.common.mediator.mediator import CommandMediator
from src.api.common.providers.stub import Stub
from src.common.dto.product import (
    Product,
    GetAllProductsQuery,
    CreateProductQuery,
    GetProductQuery,
    DeleteProductQuery,
    UpdateProductQuery,
    ProductSchema,
    Products,
)

product_router = APIRouter(tags=["product"])


@product_router.post(
    "/create",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
)
async def create_product_router(
    product: ProductSchema,
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
    _: Annotated[User, Depends(Authorization(Roles.admin))],
) -> OkResponse[Product]:
    product_result = await mediator.send(CreateProductQuery(**product.model_dump()))
    return OkResponse(product_result)


@product_router.get("", response_model=Product, status_code=status.HTTP_200_OK)
async def get_product_router(
    product_id: int,
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
    _: Annotated[User, Depends(Authorization(Roles.admin))],
) -> OkResponse[Product]:
    product = await mediator.send(GetProductQuery(id=product_id))
    return OkResponse(product)


@product_router.get("/all", response_model=Products, status_code=status.HTTP_200_OK)
async def get_all_products(
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
    _: Annotated[User, Depends(Authorization(Roles.admin))],
    limit: Optional[int | None] = None,
    offset: Optional[int | None] = None,
) -> OkResponse[Products]:
    products = await mediator.send(GetAllProductsQuery(limit=limit, offset=offset))
    return OkResponse(products)


@product_router.put("/update", response_model=Product, status_code=status.HTTP_200_OK)
async def update_product_router(
    product: Product,
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
    _: Annotated[User, Depends(Authorization(Roles.admin))],
) -> OkResponse[Product]:
    product_result = await mediator.send(UpdateProductQuery(**product.model_dump()))
    return OkResponse(product_result)


@product_router.delete(
    "/delete",
    response_model=Product,
    status_code=status.HTTP_200_OK,
)
async def delete_product_router(
    product_id: int,
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
    _: Annotated[User, Depends(Authorization(Roles.admin))],
) -> OkResponse[Product]:
    product = await mediator.send(DeleteProductQuery(id=product_id))
    return OkResponse(product)
