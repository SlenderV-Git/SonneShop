from typing import Callable

from secrets import token_hex
from faker import Faker
import pytest

from src.common.exceptions.routers import NotFoundException
from src.api.v1.handlers.auth.login import Login
from src.cache.core.client import RedisClient
from src.common.dto.token import TokensExpire
from src.database.gateway import DBGateway
from src.services.security.argon_hasher import Argon2
from src.services.security.jwt_token import TokenJWT
from src.common.dto import UserSchema, LoginShema


class TestLogin:
    @pytest.mark.asyncio
    async def test_login(
        self,
        gateway: DBGateway,
        redis: RedisClient,
        jwt: TokenJWT,
        hasher: Argon2,
        user_dto: UserSchema,
    ):
        login = Login()
        login_schema = LoginShema(
            fingerprint=token_hex(16), login=user_dto.login, password=user_dto.password
        )
        tokens = await login(
            login_data=login_schema,
            database=gateway,
            cache=redis,
            jwt=jwt,
            hasher=hasher,
        )
        assert isinstance(tokens, TokensExpire)

    @pytest.mark.asyncio
    async def test_unknown_user_login(
        self,
        gateway: DBGateway,
        redis: RedisClient,
        jwt: TokenJWT,
        hasher: Argon2,
        faker: Faker,
    ):
        login = Login()
        login_schema = LoginShema(
            fingerprint=token_hex(16), login=faker.name(), password=faker.password()
        )
        with pytest.raises(NotFoundException) as not_found:
            await login(
                login_data=login_schema,
                database=gateway,
                cache=redis,
                jwt=jwt,
                hasher=hasher,
            )
            assert not_found.message == f"User {login_schema.login} not found"
