from typing import Any

from pydantic import HttpUrl

from src.services.payment.base import BasePaymentsProtocol
from src.services.security.crypto_hasher import SignatureHasher
from src.api.v1.handlers.command.base import Command
from src.common.dto.transaction import CreatePaymentQuery, Transaction, SignatureSchema
from src.services.gateway import ServicesGateway


class PaymentCreateCommand(Command[CreatePaymentQuery, HttpUrl]):
    __slots__ = "_gateway"

    def __init__(self, service_gateway: ServicesGateway) -> None:
        self._gateway = service_gateway

    async def execute(
        self,
        query: CreatePaymentQuery,
        crypto_hasher: SignatureHasher,
        payments: BasePaymentsProtocol,
        **kwargs: Any
    ) -> HttpUrl:
        async with self._gateway:
            await self._gateway._database.manager.create_transaction()
            transaction = await self._gateway.transaction().create(
                query.user_id, Transaction(**query.model_dump())
            )
            payment_data = SignatureSchema(id=transaction.id, **query.model_dump())
            signature = crypto_hasher.generate(payment_data)
            print(signature)
            return await payments.get_payment_url(payment_data)
