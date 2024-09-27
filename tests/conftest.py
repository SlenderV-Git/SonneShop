import pytest_asyncio

from backend.database.core.connection import create_async_session_maker, create_engine
from backend.database.core.manager import TransactionManager
from backend.database.factory import create_database_factory
from backend.database.models.base.core import Base


@pytest_asyncio.fixture(autouse=True, scope="session", loop_scope="session")
async def gateway():
    engine = create_engine('sqlite+aiosqlite:///example.db')
    session = create_async_session_maker(engine)
    db_factory = create_database_factory(TransactionManager, session)

    gateway = db_factory()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
    
    async with gateway:
        await gateway.manager.create_transaction()
        
        yield gateway
        
        await gateway.manager.close_transaction()