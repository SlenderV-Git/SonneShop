from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.common.dto import User, Balance, BuyProductQuery, BuyInfo
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
    TransactionsResponse,
    SelectTransactionsQuery,
)
from src.api.v1.docs.payment import (
    CREATE_DESCRIPTION,
    CREATE_RESPONCE,
    CREATE_SUMMARY,
    WEBHOOK_DESCRIPTION,
    WEBHOOK_RESPONCE,
    WEBHOOK_SUMMARY,
    TRANSACTION_DESCRIPTION,
    TRANSACTION_RESPONCE,
    TRANSACTION_SUMMARY,
    BUY_RESPONCE,
    BUY_DESCRIPTION,
    BUY_SUMMARY,
)

payment_router = APIRouter(tags=["payment"])


@payment_router.post(
    "/create",
    response_model=PaymentUrl,
    status_code=status.HTTP_201_CREATED,
    response_description=CREATE_RESPONCE,
    description=CREATE_DESCRIPTION,
    summary=CREATE_SUMMARY,
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
    "/webhook",
    response_model=Transaction,
    status_code=status.HTTP_202_ACCEPTED,
    response_description=WEBHOOK_RESPONCE,
    description=WEBHOOK_DESCRIPTION,
    summary=WEBHOOK_SUMMARY,
)
async def approve_payment(
    body: ApprovePaymentQuery,
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
    crypto_hasher: Annotated[SignatureHasher, Depends(Stub(SignatureHasher))],
) -> Transaction:
    transaction = await mediator.send(body, crypto_hasher=crypto_hasher)
    return OkResponse(transaction)


@payment_router.get(
    "/transactions",
    response_model=TransactionsResponse,
    status_code=status.HTTP_200_OK,
    response_description=TRANSACTION_RESPONCE,
    description=TRANSACTION_DESCRIPTION,
    summary=TRANSACTION_SUMMARY,
)
async def get_all_transactions(
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
    user: Annotated[User, Depends(Authorization())],
) -> OkResponse[TransactionsResponse]:
    transactions = await mediator.send(SelectTransactionsQuery(user_id=user.id))
    return OkResponse(transactions)


@payment_router.post(
    "/buy_product",
    response_model=Balance,
    status_code=status.HTTP_200_OK,
    response_description=BUY_RESPONCE,
    description=BUY_DESCRIPTION,
    summary=BUY_SUMMARY,
)
async def buy_product(
    info: BuyInfo,
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
    user: Annotated[User, Depends(Authorization())],
) -> OkResponse[Balance]:
    balance = await mediator.send(BuyProductQuery(user_id=user.id, **info.model_dump()))
    return OkResponse(balance)
