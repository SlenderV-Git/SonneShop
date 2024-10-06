from pydantic import BaseModel, HttpUrl


class Transaction(BaseModel):
    amount: int
    account_id: int


class TransactionWithStatus(Transaction):
    approved: bool


class TransactionsResponse(BaseModel):
    transactions: list[TransactionWithStatus]


class PaymentUrl(BaseModel):
    url: HttpUrl


class TransactionSchema(Transaction):
    id: int


class PaymentData(BaseModel):
    user_id: int
    account_id: int
    amount: int


class SignatureSchema(PaymentData):
    id: int

    def __str__(self) -> str:
        return ":".join([str(arg) for arg in self.model_dump().values()])


class PaymentDataWithSignature(PaymentData):
    signature: str

    def __str__(self) -> str:
        return ":".join(
            [str(arg) for arg in self.model_dump(exclude={"signature"}).values()]
        )


class CreatePaymentQuery(PaymentData):
    pass


class SelectTransactionsQuery(BaseModel):
    user_id: int


class ApprovePaymentQuery(PaymentDataWithSignature):
    transaction_id: int
