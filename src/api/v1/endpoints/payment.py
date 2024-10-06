from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.common.dto.user import User
from src.services.payment.base import BasePaymentsProtocol
from src.services.security.crypto_hasher import SignatureHasher
from src.api.v1.handlers.auth.auth import Authorization
from src.api.common.responses import OkResponse
from src.api.common.mediator.mediator import CommandMediator
from src.api.common.providers.stub import Stub
from src.common.dto.transaction import (
    CreatePaymentQuery,
    ApprovePaymentQuery,
    Transaction,
    PaymentUrl,
)

payment_router = APIRouter(tags=["payment"])


@payment_router.post(
    "/create",
    response_model=PaymentUrl,
    status_code=status.HTTP_201_CREATED,
)
async def create_payment(
    body: Transaction,
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
    crypto_hasher: Annotated[SignatureHasher, Depends(Stub(SignatureHasher))],
    payments: Annotated[BasePaymentsProtocol, Depends(Stub(BasePaymentsProtocol))],
    user: Annotated[User, Depends(Authorization())],
) -> OkResponse[PaymentUrl]:
    payment_query = CreatePaymentQuery(user_id=user.id, **body.model_dump())
    payment_url = await mediator.send(
        payment_query, crypto_hasher=crypto_hasher, payments=payments
    )
    return OkResponse(payment_url, status_code=201)


@payment_router.post(
    "/webhook", response_model=Transaction, status_code=status.HTTP_202_ACCEPTED
)
async def approve_payment(
    body: ApprovePaymentQuery,
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
    crypto_hasher: Annotated[SignatureHasher, Depends(Stub(SignatureHasher))],
) -> Transaction:
    transaction = await mediator.send(body, crypto_hasher=crypto_hasher)
    return OkResponse(transaction)
