from typing import Optional, Sequence
from pydantic import BaseModel, model_validator

from src.common.exceptions.services import WarehouseError


class ProductStock(BaseModel):
    product_id: int
    remaining: int


class ProductStockDB(ProductStock):
    @model_validator(mode="after")
    def check_remainings(self) -> int:
        if self.remaining < 0:
            raise WarehouseError(
                f"There are not enough items with id №{self.product_id} in stock to write off"
            )
        return self


class ProductDTO(ProductStock):
    title: str
    description: str
    price: int


class Warehouse(BaseModel):
    products: Sequence[ProductDTO]


class ConductInventoryWarehouse(BaseModel):
    limit: Optional[int | None] = None
    offset: Optional[int | None] = None
