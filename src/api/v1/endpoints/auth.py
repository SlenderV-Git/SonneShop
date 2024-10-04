from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.api.common.responses import OkResponse
from src.api.v1.handlers.auth import Login, Authorization, Logout
from src.common.dto import Token, TokensExpire, Status

auth_router = APIRouter(tags=["auth"])


@auth_router.post(
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
        value=login.refresh_token,
        expires=login.expire_date,
        httponly=True,
        secure=True,
    )
    return response


@auth_router.post("/reflesh", response_model=Token, status_code=status.HTTP_200_OK)
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


@auth_router.post("/logout", response_model=Status)
async def logout_router(
    status: Annotated[Status, Depends(Logout())],
) -> OkResponse[Status]:
    response = OkResponse(status)
    response.delete_cookie("refresh_token")

    return response
