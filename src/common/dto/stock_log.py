from pydantic import BaseModel

from src.common.enum.operation import OperationType


class StockOperation(BaseModel):
    product_id: int
    quantity: int
    type_operation: OperationType


class Stock(BaseModel):
    operations: StockOperation
