from src.common.dto.base import DTO


class ProductSchema(DTO):
    title: str
    description: str
    price: int


class Product(ProductSchema):
    id: int
