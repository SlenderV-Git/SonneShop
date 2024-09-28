import pytest
from backend.common.dto.user import UserSchema
from backend.database.gateway import DBGateway
from backend.database.models import UserModel


class TestUserRepository:
    @pytest.mark.asyncio
    async def test_user_create(self, user: UserModel, user_dto: UserSchema):
        assert user.login == user_dto.login
        assert user.email == user_dto.email

    @pytest.mark.asyncio
    async def test_user_update(self, gateway: DBGateway, user: UserModel):
        new_email = "new_example@gmail.com"
        new_user = await gateway.user().update(user.id, email=new_email)
        assert new_user.email == new_email

    @pytest.mark.asyncio
    async def test_user_delete(
        self, gateway: DBGateway, user: UserModel, user_dto: UserSchema
    ):
        await gateway.user().delete(user.id)
        user = await gateway.user().get_one(login=user_dto.login)
        assert user is None
