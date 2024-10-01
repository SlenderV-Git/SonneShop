from src.common.interfaces.gateway import BaseGateway
from src.database.gateway import DBGateway
from src.services.user import UserService


class ServicesGateway(BaseGateway):
    __slots__ = "_database"

    def __init__(self, database: DBGateway) -> None:
        self._database = database
        super().__init__(database)

    def user(self) -> UserService:
        return UserService(repository=self._database.user())
