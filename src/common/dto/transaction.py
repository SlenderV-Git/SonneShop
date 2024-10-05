from pydantic import BaseModel


class PaymentData(BaseModel):
    transaction_id: int
    user_id: int
    bill_id: int
    amount: int

    def __str__(self) -> str:
        return ":".join([str(arg) for arg in self.model_dump().values()])


class PaymentDataWithSignature(PaymentData):
    signature: str

    def __str__(self) -> str:
        return ":".join(
            [str(arg) for arg in self.model_dump(exclude={"signature"}).values()]
        )
