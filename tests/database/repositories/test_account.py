import pytest
from random import randrange

from backend.database.gateway import DBGateway
from backend.database.models.account import AccountModel
from backend.database.models.user import UserModel


class TestAccountRepository:
    @pytest.mark.asyncio
    async def test_account_count(self, gateway: DBGateway, user : UserModel):
        account_count = 3
        assert len(await gateway.account().get_all(user.id)) == account_count
    
    @pytest.mark.asyncio
    async def test_account_deposit(self, gateway: DBGateway, accounts : list[AccountModel]):
        for account in accounts:
            amount = randrange(1, 1000)
            deposit_account = await gateway.account(
                ).update(
                    account.id, 
                    amount
                )
            
            assert deposit_account.balance == amount
    
    @pytest.mark.asyncio
    async def test_account_delete(
            self, 
            gateway: DBGateway, 
            accounts : list[AccountModel],
            user : UserModel
    ):
        for account in accounts:
            await gateway.account().delete(account.id)
            
        assert await gateway.account().get_all(user.id) == []