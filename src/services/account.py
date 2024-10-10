from typing import Sequence
from src.common.exceptions.services import AccountError, NotFoundError
from src.common.dto.account import Account, Balance
from src.common.interfaces.gateway import BaseGateway
from src.database.repositories.account import AccountRepository
from src.database.converter import from_model_to_dto, from_list_model_to_list_dto


class AccountService(BaseGateway):
    __slots__ = "_repository"

    def __init__(self, repository: AccountRepository) -> None:
        self._repository = repository

    async def create(self, user_id: int) -> Account:
        accounts = await self.get_all_accounts(user_id)
        if len(accounts) >= 3:
            raise AccountError("You cannot create more than 3 bill for 1 account")
        return from_model_to_dto(
            await self._repository.create(user_id=user_id), Balance
        )

    async def get_balance_all(self, user_id: int) -> Balance:
        accounts = await self._repository.get_all(user_id)
        return Balance(balance=sum([account.balance for account in accounts]))

    async def get_all_accounts(self, user_id: int) -> Sequence[Account]:
        return from_list_model_to_list_dto(
            await self._repository.get_all(user_id), Account
        )

    async def get_balance(self, user_id: int, account_id: int) -> Balance:
        account = await self._repository.get_one(user_id=user_id, account_id=account_id)
        if not account:
            raise NotFoundError("Failed to retrieve. Account not find")

        return from_model_to_dto(account, Balance)

    async def replenish(
        self, user_id: int, account_id: int, amount: int, **kw
    ) -> Balance:
        account = await self._repository.update(
            user_id=user_id, account_id=account_id, amount=amount
        )
        if not account:
            raise NotFoundError("Account not found")

        return from_model_to_dto(account, Balance)

    async def delete_account(self, user_id: int, account_id: int) -> Account:
        account = await self._repository.delete(user_id, account_id)
        if not account:
            raise NotFoundError("Failed to delete. Account not find")

        return from_model_to_dto(account, Account)
