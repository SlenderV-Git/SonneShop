from typing import Optional, Sequence

from pydantic import model_validator
from src.common.exceptions.services import ValidationError
from src.common.dto.base import DTO


class ProductSchema(DTO):
    title: str
    description: str
    price: int


class ProductId(DTO):
    id: int


class Product(ProductSchema, ProductId):
    @model_validator(mode="after")
    def check_price(self) -> int:
        if self.price < 0:
            raise ValidationError("The price of a product cannot be negative")
        return self


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
