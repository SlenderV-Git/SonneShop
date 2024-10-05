from typing import Sequence
from common.dto.product import Product, ProductSchema
from common.exceptions.services import ConflictError, NotFoundError
from common.interfaces.gateway import BaseGateway
from database.repositories.product import ProductRepostory
from src.database.converter import from_model_to_dto, from_list_model_to_list_dto


class ProductService(BaseGateway):
    __slots__ = "_repository"

    def __init__(self, repository: ProductRepostory) -> None:
        self._repository = repository

    async def create(self, data: ProductSchema) -> Product:
        product = self._repository.create(**data.model_dump())
        if not product:
            raise ConflictError(f"Product {data.title} is already exists")

        return from_model_to_dto(product, Product)

    async def update(self, product_id: int, data: ProductSchema) -> Product:
        product = await self._repository.update(
            product_id=product_id, **data.model_dump()
        )
        if not product:
            raise NotFoundError(f"Failed to update. Product {data.title} not found")

        return from_model_to_dto(product, Product)

    async def get(self, product_id: int) -> Product:
        product = await self._repository.get_one(product_id)
        if not product:
            raise NotFoundError("Failed to get. Product not found")

        return from_model_to_dto(product, Product)

    async def get_all(self, offset: int = None, limit: int = None) -> Sequence[Product]:
        products = await self._repository.get_all(offset, limit)
        return from_list_model_to_list_dto(products, Product)

    async def delete(self, product_id: int) -> Product:
        product = await self._repository.delete(product_id)
        if not product:
            raise NotFoundError("Failed to get. Product not found")

        return from_model_to_dto(product, Product)
