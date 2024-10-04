import copy
from typing import Callable

import pytest
import pytest_asyncio
from faker import Faker
from faker.providers import internet
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from fakeredis.aioredis import FakeRedis

from src.api.common.mediator.mediator import CommandMediator
from src.cache.core.client import RedisClient
from src.core.settings import get_jwt_settings
from src.database.gateway import DBGateway
from src.services.factory import create_service_gateway_factory
from src.services.gateway import ServicesGateway
from src.services.security.argon_hasher import Argon2, get_argon2_hasher
from src.services.security.jwt_token import TokenJWT
from src.common.dto.user import UserSchema
from src.database.core.connection import create_async_session_maker, create_engine
from src.database.core.manager import TransactionManager
from src.database.factory import create_database_factory
from src.database.models.base.core import Base


@pytest.fixture(autouse=True, scope="session")
def faker():
    fake = Faker()
    fake.add_provider(internet)
    return fake


@pytest_asyncio.fixture(autouse=True, scope="session", loop_scope="session")
async def engine():
    return create_engine("sqlite+aiosqlite:///:memory:")


@pytest_asyncio.fixture(autouse=True, scope="session", loop_scope="session")
async def session(engine: AsyncEngine):
    session = create_async_session_maker(engine)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()

    return session


@pytest_asyncio.fixture(autouse=True, scope="session", loop_scope="session")
async def gateway_factory(session: AsyncSession):
    db_factory = create_database_factory(TransactionManager, session)
    return db_factory


@pytest_asyncio.fixture(autouse=True, scope="session", loop_scope="session")
async def gateway(gateway_factory: Callable[[], DBGateway]):
    gateway = gateway_factory()

    async with gateway:
        await gateway.manager.create_transaction()

        yield gateway

        await gateway.manager.close_transaction()


@pytest.fixture(autouse=True, scope="session")
def user_dto(faker: Faker):
    return UserSchema(
        login=faker.name(),
        email=faker.email(safe=True),
        password=faker.password(length=10),
    )


@pytest_asyncio.fixture(autouse=True, scope="session", loop_scope="session")
async def user(
    gateway: DBGateway,
    user_dto: UserSchema,
    service_gateway: Callable[[], ServicesGateway],
    hasher: Argon2,
):
    await service_gateway().user().create(copy.deepcopy(user_dto), hasher=hasher)
    return await gateway.user().get_one(login=user_dto.login)


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
