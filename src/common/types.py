from typing import TypeVar

ModelType = TypeVar("ModelType", bound="Base")  # noqa: F821
ResultType = TypeVar("ResultType")
SessionFactory = TypeVar("SessionFactory")
GatewayType = TypeVar("GatewayType", bound="BaseGateway")  # noqa: F821
RepositoryType = TypeVar("RepositoryType")
DependencyType = TypeVar("DependencyType")
