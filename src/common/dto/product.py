from typing import Optional, Sequence
from src.common.dto.base import DTO


class ProductSchema(DTO):
    title: str
    description: str
    price: int


class ProductId(DTO):
    id: int


class Product(ProductSchema, ProductId):
    pass


class Products(DTO):
    products: Sequence[Product]


class CreateProductQuery(ProductSchema):
    pass


class UpdateProductQuery(ProductSchema, ProductId):
    pass


class GetProductQuery(ProductId):
    pass


class GetAllProductsQuery(DTO):
    limit: Optional[int | None] = None
    offset: Optional[int | None] = None


class DeleteProductQuery(ProductId):
    pass
