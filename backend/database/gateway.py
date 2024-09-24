from typing import Type
from backend.common.interfaces.gateway import BaseGateway
from backend.common.types import RepositoryType
from backend.database.core.manager import TransactionManager


class DBGateway(BaseGateway):
    def __init__(self, manager: TransactionManager) -> None:
        self.manager = manager
        super().__init__(manager)
        
    def _init_repo(self, cls: Type[RepositoryType]) -> RepositoryType:
        return cls(self.manager.session)