import pytest
from random import randrange

from src.database.gateway import DBGateway
from src.database.models.account import AccountModel
from src.database.models.user import UserModel


class TestAccountRepository:
    @pytest.mark.asyncio
    async def test_account_count(self, gateway: DBGateway, user: UserModel):
        accounts = await gateway.account().get_all(user.id)
        assert len(accounts) == 3

    @pytest.mark.asyncio
    async def test_account_deposit(
        self, gateway: DBGateway, accounts: list[AccountModel], user: UserModel
    ):
        for account in accounts:
            amount = randrange(1, 1000)
            deposit_account = await gateway.account().update(
                user.id, account.id, amount
            )
            assert deposit_account.balance == amount

    @pytest.mark.asyncio
    async def test_account_delete(
        self, gateway: DBGateway, accounts: list[AccountModel], user: UserModel
    ):
        for account in accounts:
            await gateway.account().delete(user.id, account.id)

        assert await gateway.account().get_all(user.id) == []
