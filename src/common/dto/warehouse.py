from typing import Optional, Sequence
from pydantic import BaseModel


class ProductStock(BaseModel):
    product_id: int
    remaining: int


class ProductDTO(ProductStock):
    title: str
    description: str
    price: int


class Warehouse(BaseModel):
    products: Sequence[ProductDTO]


class ConductInventoryWarehouse(BaseModel):
    limit: Optional[int | None] = None
    offset: Optional[int | None] = None
