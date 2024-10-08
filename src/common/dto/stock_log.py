from typing import Sequence
from pydantic import BaseModel

from src.common.enum.operation import OperationType


class StockOperation(BaseModel):
    product_id: int
    quantity: int
    type_operation: OperationType


class Stock(BaseModel):
    operations: list[StockOperation]


class ConductMassUpdateStockpile(BaseModel):
    products: Sequence[StockOperation]


class AddProductsqQuery(Stock):
    pass


class UpdateProductStock(StockOperation):
    pass


class GetProductMovement(BaseModel):
    product_id: int
