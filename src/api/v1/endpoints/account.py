from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.common.dto.user import User
from src.api.v1.handlers.auth.auth import Authorization
from src.api.common.responses import OkResponse
from src.api.common.mediator.mediator import CommandMediator
from src.api.common.providers.stub import Stub
from src.common.dto import (
    AccountBalanceQuery,
    AllAccountsBalanceQuery,
    AccountCreateQuery,
    Balance,
)
from src.api.v1.docs.account import (
    CREATE_DESCRIPTION,
    CREATE_RESPONCE,
    CREATE_SUMMARY,
    BALANCE_DESCRIPTION,
    BALANCE_RESPONCE,
    BALANCE_SUMMARY,
    BALANCES_DESCRIPTION,
    BALANCES_RESPONCE,
    BALANCES_SUMMARY,
)

account_router = APIRouter(tags=["bill"])


@account_router.post(
    "/create",
    response_model=Balance,
    status_code=status.HTTP_201_CREATED,
    response_description=CREATE_RESPONCE,
    description=CREATE_DESCRIPTION,
    summary=CREATE_SUMMARY,
)
async def create_bill_router(
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
    user: Annotated[User, Depends(Authorization())],
) -> OkResponse[Balance]:
    balance = await mediator.send(AccountCreateQuery(user_id=user.id))
    return OkResponse(balance, status_code=201)


@account_router.get(
    "/balance",
    response_model=Balance,
    status_code=status.HTTP_200_OK,
    response_description=BALANCE_RESPONCE,
    description=BALANCE_DESCRIPTION,
    summary=BALANCE_SUMMARY,
)
async def get_balance_router(
    bill_id: int,
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
    user: Annotated[User, Depends(Authorization())],
) -> OkResponse[Balance]:
    balance = await mediator.send(AccountBalanceQuery(user_id=user.id, id=bill_id))
    return OkResponse(balance)


@account_router.get(
    "/all",
    response_model=Balance,
    status_code=status.HTTP_200_OK,
    response_description=BALANCES_RESPONCE,
    description=BALANCES_DESCRIPTION,
    summary=BALANCES_SUMMARY,
)
async def get_balance_all_bills_router(
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
    user: Annotated[User, Depends(Authorization())],
) -> OkResponse[Balance]:
    balance = await mediator.send(AllAccountsBalanceQuery(user_id=user.id))
    return OkResponse(balance)
