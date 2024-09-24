from typing import Callable, Type
from backend.common.types import SessionFactory
from backend.database.core.manager import TransactionManager
from backend.database.gateway import DBGateway


def create_database_factory(
        manager : Type[TransactionManager], 
        session_factory : SessionFactory
) -> Callable[[], DBGateway]:
    def _create() -> DBGateway:
        return DBGateway(manager(session_factory))
    
    return _create