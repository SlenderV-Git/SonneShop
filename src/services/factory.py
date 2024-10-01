from typing import Callable
from src.database.gateway import DBGateway
from src.services.gateway import ServicesGateway


def create_service_gateway_factory(
    database: Callable[[], DBGateway]
) -> ServicesGateway:
    def _create():
        return ServicesGateway(database=database())

    return _create
