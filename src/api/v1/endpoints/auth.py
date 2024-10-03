from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.common.dto.healthcheck import HealthCheckResponseSchema
from src.api.common.responses import OkResponse
from src.api.v1.handlers.auth import Login, Authorization
from src.common.dto import Token, TokensExpire

auth_router = APIRouter(tags=["auth"])


@auth_router.get(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
)
async def login_endpoint(
    login: Annotated[TokensExpire, Depends(Login())]
) -> OkResponse[Token]:
    response = OkResponse(Token(token=login.acces_token))
    response.set_cookie(
        "refresh_token",
        value=login.reflesh_token,
        expires=login.expire_date,
        httponly=True,
        secure=True,
    )
    return response


@auth_router.get(
    "/reflesh", response_model=HealthCheckResponseSchema, status_code=status.HTTP_200_OK
)
async def reflesh_endpoint(
    user: Annotated[bool, Depends(Authorization().verify_refresh)]
) -> HealthCheckResponseSchema:
    return HealthCheckResponseSchema(ok=user)
