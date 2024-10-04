from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.api.v1.handlers.auth.auth import Authorization
from src.api.common.responses import OkResponse
from src.services.security.argon_hasher import Argon2
from src.api.common.mediator.mediator import CommandMediator
from src.api.common.providers.stub import Stub
from src.common.dto import User, UserSchema, SelectUserQuery

user_router = APIRouter(tags=["user"])


@user_router.post(
    "/reg",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
)
async def user_reg_router(
    body: UserSchema,
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
    hasher: Annotated[Argon2, Depends(Stub(Argon2))],
):
    user: User = await mediator.send(body, hasher=hasher)
    return OkResponse(user, status_code=status.HTTP_201_CREATED)


@user_router.get("/me", response_model=User, status_code=status.HTTP_200_OK)
async def get_me_router(
    body: Annotated[User, Depends(Authorization())],
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
):
    user = await mediator.send(SelectUserQuery(id=body.id))
    return OkResponse(user)
