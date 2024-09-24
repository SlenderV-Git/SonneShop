from typing import TypeVar

from backend.common.interfaces.gateway import BaseGateway


ModelType = TypeVar("ModelType", bound="Base")  # noqa: F821
SessionFactory = TypeVar("SessionFactory")
GatewayType = TypeVar("GatewayType", bound=BaseGateway)
RepositoryType = TypeVar("RepositoryType")
