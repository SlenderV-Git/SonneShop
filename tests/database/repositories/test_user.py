import pytest
import pytest_asyncio
from backend.common.dto.user import UserSchema
from backend.database.gateway import DBGateway
from backend.database.models import UserModel

class TestUserRepository:
    login = "Victor"
    email = "example@gmail.com"
    password = "H2aaddMMSNASK4"

    @pytest_asyncio.fixture(autouse=True, scope="session", loop_scope="session")
    async def user(self, gateway: DBGateway):
        user = UserSchema(
            login=self.login,
            email=self.email,
            password=self.password
        )
        await gateway.user().create(**user.model_dump())
        return await gateway.user().get_one(login=self.login)

    @pytest.mark.asyncio
    async def test_user_create(self, user : UserModel):
        assert user.login == self.login
        assert user.email == self.email

    @pytest.mark.asyncio
    async def test_user_update(self, gateway: DBGateway, user : UserModel):
        new_email = "new_example@gmail.com"
        new_user = await gateway.user().update(user.id, email=new_email)
        assert new_user.email == new_email

    @pytest.mark.asyncio
    async def test_user_delete(self, gateway: DBGateway, user  : UserModel):
        await gateway.user().delete(user.id)
        user = await gateway.user().get_one(login=self.login)
        assert user is None
