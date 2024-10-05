from typing import Type
from src.common.interfaces.gateway import BaseGateway
from src.common.types import RepositoryType
from src.database.core.manager import TransactionManager
from src.database.repositories import (
    UserRepository,
    AccountRepository,
    ProductRepostory,
    TransactionRepostory,
)


class DBGateway(BaseGateway):
    def __init__(self, manager: TransactionManager) -> None:
        self.manager = manager
        super().__init__(manager)

    def account(self):
        return self._init_repo(AccountRepository)

    def user(self):
        return self._init_repo(UserRepository)

    def product(self):
        return self._init_repo(ProductRepostory)

    def transaction(self):
        return self._init_repo(TransactionRepostory)

    def _init_repo(self, cls: Type[RepositoryType]) -> RepositoryType:
        return cls(self.manager.session)
