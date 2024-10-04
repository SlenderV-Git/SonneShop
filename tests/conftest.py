from typing import Callable
import pytest
import pytest_asyncio
from faker import Faker
from faker.providers import internet
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.database.gateway import DBGateway
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
    return create_engine("sqlite+aiosqlite:///example.db")


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
