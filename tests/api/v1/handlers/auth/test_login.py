import pytest

from src.common.exceptions.routers import NotFoundException
from src.api.v1.handlers.auth.login import Login
from src.cache.core.client import RedisClient
from src.common.dto.token import TokensExpire
from src.database.gateway import DBGateway
from src.services.security.argon_hasher import Argon2
from src.services.security.jwt_token import TokenJWT
from src.common.dto import LoginShema


class TestLogin:
    @pytest.mark.asyncio
    async def test_login(self, auth_tokens: TokensExpire):
        assert isinstance(auth_tokens, TokensExpire)

    @pytest.mark.asyncio
    async def test_unknown_user_login(
        self,
        gateway: DBGateway,
        redis: RedisClient,
        jwt: TokenJWT,
        hasher: Argon2,
        fake_login_schema: LoginShema,
    ):
        login = Login()

        with pytest.raises(NotFoundException) as not_found:
            await login(
                login_data=fake_login_schema,
                database=gateway,
                cache=redis,
                jwt=jwt,
                hasher=hasher,
            )
            assert not_found.message == f"User {fake_login_schema.login} not found"
