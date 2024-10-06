import secrets
from faker import Faker
from pydantic import HttpUrl

from src.common.dto.transaction import PaymentDataWithSignature
from src.services.payment.base import BasePaymentsProtocol


class ExamplePayment(BasePaymentsProtocol[PaymentDataWithSignature, HttpUrl]):
    async def get_payment_url(self, data: PaymentDataWithSignature) -> HttpUrl:
        return Faker().url() + secrets.token_hex(16)


def get_example_payment_client():
    return ExamplePayment()
