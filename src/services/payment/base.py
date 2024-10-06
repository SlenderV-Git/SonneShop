from typing import Generic, Protocol, TypeVar
from abc import abstractmethod

from pydantic import HttpUrl

DT = TypeVar("DataType")
PU = TypeVar("PaymentUrl", bound=HttpUrl)


class BasePaymentsProtocol(Protocol, Generic[DT, PU]):
    @abstractmethod
    async def get_payment_url(self, data: DT) -> PU:
        ...
