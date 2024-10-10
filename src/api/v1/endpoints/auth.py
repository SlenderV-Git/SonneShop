from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.api.common.responses import OkResponse
from src.api.v1.handlers.auth import Login, Authorization, Logout
from src.common.dto import Token, TokensExpire, Status
from src.api.v1.docs.auth import (
    AUTH_DESCRIPTION,
    AUTH_RESPONCE,
    AUTH_SUMMARY,
    REFRESH_DESCRIPTION,
    REFRESH_RESPONCE,
    REFRESH_SUMMARY,
    LOGOUT_DESCRIPTION,
    LOGOUT_RESPONCE,
    LOGOUT_SUMMARY,
)

auth_router = APIRouter(tags=["auth"])


@auth_router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    response_description=AUTH_RESPONCE,
    description=AUTH_DESCRIPTION,
    summary=AUTH_SUMMARY,
)
async def login_endpoint(
    login: Annotated[TokensExpire, Depends(Login())]
) -> OkResponse[Token]:
    response = OkResponse(Token(token=login.acces_token))
    response.set_cookie(
        "refresh_token",
        value=login.refresh_token,
        expires=login.expire_date,
        httponly=True,
        secure=True,
    )
    return response


@auth_router.post(
    "/reflesh",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    response_description=REFRESH_RESPONCE,
    description=REFRESH_DESCRIPTION,
    summary=REFRESH_SUMMARY,
)
async def refresh_endpoint(
    refresh: Annotated[TokensExpire, Depends(Authorization().verify_refresh)]
) -> OkResponse[Token]:
    response = OkResponse(Token(token=refresh.acces_token))
    response.set_cookie(
        "refresh_token",
        value=refresh.refresh_token,
        expires=refresh.expire_date,
        httponly=True,
        secure=True,
    )
    return response


@auth_router.post(
    "/logout",
    response_model=Status,
    response_description=LOGOUT_RESPONCE,
    description=LOGOUT_DESCRIPTION,
    summary=LOGOUT_SUMMARY,
)
async def logout_router(
    status: Annotated[Status, Depends(Logout())],
) -> OkResponse[Status]:
    response = OkResponse(status)
    response.delete_cookie("refresh_token")

    return response
