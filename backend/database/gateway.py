from typing import Type
from backend.common.interfaces.gateway import BaseGateway
from backend.common.types import RepositoryType
from backend.database.core.manager import TransactionManager
from backend.database.repositories import UserRepository, AccountRepository


class DBGateway(BaseGateway):
    def __init__(self, manager: TransactionManager) -> None:
        self.manager = manager
        super().__init__(manager)
        
    def account(self):
        return self._init_repo(AccountRepository)
        
    def user(self):
        return self._init_repo(UserRepository)
        
    def _init_repo(self, cls: Type[RepositoryType]) -> RepositoryType:
        return cls(self.manager.session)