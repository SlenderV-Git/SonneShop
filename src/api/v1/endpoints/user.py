from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.api.v1.handlers.auth.auth import Authorization
from src.api.common.responses import OkResponse
from src.services.security.argon_hasher import Argon2
from src.api.common.mediator.mediator import CommandMediator
from src.api.common.providers.stub import Stub
from src.api.v1.docs.user import (
    REG_RESPONCE,
    REG_DESCRIPTION,
    REG_SUMMARY,
    ME_DESCRIPTION,
    ME_RESPONCE,
    ME_SUMMARY,
    UPDATE_DESCRIPTION,
    UPDATE_RESPONCE,
    UPDATE_SUMMARY,
)
from src.common.dto import (
    User,
    UserSchema,
    SelectUserQuery,
    UpdateUserQuery,
    UserResponse,
)

user_router = APIRouter(tags=["user"])


@user_router.post(
    "/reg",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    response_description=REG_RESPONCE,
    description=REG_DESCRIPTION,
    summary=REG_SUMMARY,
)
async def user_reg_router(
    body: UserSchema,
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
    hasher: Annotated[Argon2, Depends(Stub(Argon2))],
):
    user: UserResponse = await mediator.send(body, hasher=hasher)
    return OkResponse(user, status_code=status.HTTP_201_CREATED)


@user_router.get(
    "/me",
    response_model=User,
    status_code=status.HTTP_200_OK,
    response_description=ME_RESPONCE,
    description=ME_DESCRIPTION,
    summary=ME_SUMMARY,
)
async def get_me_router(
    body: Annotated[User, Depends(Authorization())],
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
):
    user = await mediator.send(SelectUserQuery(id=body.id))
    return OkResponse(user)


@user_router.put(
    "/update",
    response_model=User,
    status_code=status.HTTP_200_OK,
    response_description=UPDATE_RESPONCE,
    description=UPDATE_DESCRIPTION,
    summary=UPDATE_SUMMARY,
)
async def update_data_router(
    body: UserSchema,
    current: Annotated[User, Depends(Authorization())],
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
    hasher: Annotated[Argon2, Depends(Stub(Argon2))],
):
    user: User = await mediator.send(
        UpdateUserQuery(id=current.id, **body.model_dump()), hasher=hasher
    )
    return OkResponse(user)
