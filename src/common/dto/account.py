from pydantic import BaseModel, model_validator

from src.common.exceptions.services import AccountError, ValidationError


class Account(BaseModel):
    id: int
    balance: int


class Balance(BaseModel):
    balance: int

    @model_validator(mode="after")
    def check_balance(self) -> int:
        if self.balance < 0:
            raise AccountError("Insufficient funds for the transaction")
        return self


class BaseQuery(BaseModel):
    user_id: int
    id: int


class AccountCreateQuery(BaseModel):
    user_id: int


class AccountReplenishmentQuery(BaseQuery):
    amount: int


class AccountBalanceQuery(BaseQuery):
    pass


class AllAccountsBalanceQuery(BaseModel):
    user_id: int


class DeleteAccountQuery(BaseQuery):
    pass


class BuyInfo(BaseModel):
    id: int
    product_id: int
    count: int

    @model_validator(mode="after")
    def check_count(self) -> int:
        if self.count < 0:
            raise ValidationError(
                f"Unable to execute operation, quantity of good must be greater than zero"
            )
        return self


class BuyProductQuery(BuyInfo):
    user_id: int
