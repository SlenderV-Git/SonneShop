from secrets import token_hex
from faker import Faker
import pytest_asyncio

from src.cache.core.client import RedisClient
from src.database.gateway import DBGateway
from src.services.security.argon_hasher import Argon2
from src.services.security.jwt_token import TokenJWT
from src.api.v1.handlers.auth.login import Login
from src.common.dto.user import LoginShema, UserSchema


@pytest_asyncio.fixture(autouse=True, scope="session", loop_scope="session")
async def login_schema(user_dto: UserSchema):
    return LoginShema(
        fingerprint=token_hex(16), login=user_dto.login, password=user_dto.password
    )


@pytest_asyncio.fixture(autouse=True, scope="session", loop_scope="session")
async def fake_login_schema(faker: Faker):
    return LoginShema(
        fingerprint=token_hex(16), login=faker.name(), password=faker.password()
    )


@pytest_asyncio.fixture()
async def auth_tokens(
    gateway: DBGateway,
    redis: RedisClient,
    jwt: TokenJWT,
    hasher: Argon2,
    login_schema: LoginShema,
):
    login = Login()
    tokens = await login(
        login_data=login_schema,
        database=gateway,
        cache=redis,
        jwt=jwt,
        hasher=hasher,
    )
    return tokens
