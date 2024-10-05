from pydantic import BaseModel


class Account(BaseModel):
    id: int
    balance: int


class Balance(BaseModel):
    balance: int


class BaseQuery(BaseModel):
    user_id: int
    id: int


class AccountReplenishmentQuery(BaseQuery):
    amount: int


class AccountBalanceQuery(BaseQuery):
    pass


class AllAccountsBalanceQuery(BaseModel):
    pass


class DeleteAccountQuery(BaseQuery):
    pass
