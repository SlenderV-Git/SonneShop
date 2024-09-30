from typing import Callable, Type
from src.common.types import SessionFactory
from src.database.core.manager import TransactionManager
from src.database.gateway import DBGateway


def create_database_factory(
    manager: Type[TransactionManager], session_factory: SessionFactory
) -> Callable[[], DBGateway]:
    def _create() -> DBGateway:
        return DBGateway(manager(session_factory))

    return _create
