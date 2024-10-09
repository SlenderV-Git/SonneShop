from pydantic import BaseModel, model_validator

from src.common.exceptions.services import AccountError


class Account(BaseModel):
    id: int
    balance: int


class Balance(BaseModel):
    balance: int

    @model_validator(mode="after")
    def check_remainings(self) -> int:
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
