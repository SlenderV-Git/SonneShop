from typing import Callable
from fakeredis.aioredis import FakeRedis
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.api.common.mediator.mediator import CommandMediator
from src.cache.core.client import RedisClient
from src.core.settings import get_jwt_settings
from src.database.gateway import DBGateway
from src.services.factory import create_service_gateway_factory
from src.services.gateway import ServicesGateway
from src.services.security.argon_hasher import Argon2, get_argon2_hasher
from src.services.security.jwt_token import TokenJWT


@pytest_asyncio.fixture(autouse=True, scope="session", loop_scope="session")
async def service_gateway(gateway_factory: DBGateway):
    return create_service_gateway_factory(gateway_factory)


@pytest_asyncio.fixture(autouse=True, scope="session", loop_scope="session")
async def hasher():
    return get_argon2_hasher()


@pytest_asyncio.fixture(autouse=True, scope="session", loop_scope="session")
async def redis():
    return RedisClient(FakeRedis())


@pytest_asyncio.fixture(autouse=True, scope="session", loop_scope="session")
async def jwt():
    return TokenJWT(get_jwt_settings())


@pytest_asyncio.fixture(autouse=True, scope="session", loop_scope="session")
async def mediator(
    engine: AsyncEngine,
    session: AsyncSession,
    gateway_factory: Callable[[], DBGateway],
    service_gateway: ServicesGateway,
    redis: RedisClient,
    jwt: TokenJWT,
    hasher: Argon2,
):
    mediator = CommandMediator()
    mediator.setup(
        engine=engine,
        session=session,
        db_gateway=gateway_factory,
        service_gateway=service_gateway,
        redis_client=redis,
        jwt_token=jwt,
        hasher=hasher,
    )
    return mediator
