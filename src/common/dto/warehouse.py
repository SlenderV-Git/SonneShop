from typing import Sequence
from pydantic import BaseModel


class ProductStock(BaseModel):
    product_id: int
    remaining: int


class ProductDTO(ProductStock):
    title: str
    description: str
    price: int


class Warehouse(BaseModel):
    products: Sequence[ProductStock]
