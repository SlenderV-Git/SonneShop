from src.common.exceptions.services import NotFoundError
from src.common.dto.account import (
    Account,
    Balance,
    AccountBalanceQuery,
    DeleteAccountQuery,
    AccountReplenishmentQuery,
)
from src.common.interfaces.gateway import BaseGateway
from src.database.repositories.account import AccountRepository
from src.database.converter import from_model_to_dto


class AccountService(BaseGateway):
    __slots__ = "_repository"

    def __init__(self, repository: AccountRepository) -> None:
        self._repository = repository

    async def create(self, user_id: int) -> Account:
        await self._repository.create(user_id=user_id)

    async def get_balance_all(self, user_id: int) -> Balance:
        accounts = await self._repository.get_all(user_id)
        return Balance(balance=sum([account.balance for account in accounts]))

    async def get_balance(self, account_query: AccountBalanceQuery) -> Balance:
        account = await self._repository.get_one(
            user_id=account_query.user_id, account_id=account_query.id
        )
        if not account:
            raise NotFoundError("Failed to retrieve. Account not find")

        return from_model_to_dto(account, Balance)

    async def replenish(self, paid: AccountReplenishmentQuery) -> Balance:
        account = await self._repository.update(
            user_id=paid.user_id, account_id=paid.id, amount=paid.amount
        )
        if not account:
            raise NotFoundError("Failed to refill. Account not found")

        return from_model_to_dto(account, Balance)

    async def delete_account(self, account_query: DeleteAccountQuery) -> Account:
        account = await self._repository.delete(account_query.user_id, account_query.id)
        if not account:
            raise NotFoundError("Failed to delete. Account not find")

        return from_model_to_dto(account, Account)
