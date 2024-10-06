from typing import Any

from src.common.exceptions.services import InvalidSignatureError
from src.services.security.crypto_hasher import SignatureHasher
from src.api.v1.handlers.command.base import Command
from src.common.dto.transaction import ApprovePaymentQuery, Transaction
from src.services.gateway import ServicesGateway


class PaymentApproveCommand(Command[ApprovePaymentQuery, Transaction]):
    __slots__ = "_gateway"

    def __init__(self, service_gateway: ServicesGateway) -> None:
        self._gateway = service_gateway

    async def execute(
        self, query: ApprovePaymentQuery, crypto_hasher: SignatureHasher, **kwargs: Any
    ) -> Transaction:
        async with self._gateway:
            await self._gateway._database.manager.create_transaction()
            if not crypto_hasher.verify(query):
                raise InvalidSignatureError("Signature broken")

            await self._gateway.account().replenish(**query.model_dump())
            return await self._gateway.transaction().approve(query.transaction_id)
