from typing import Annotated, Any, Literal, Optional

from fastapi import Depends, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.openapi.models import HTTPBearer as HTTPBearerModel
from fastapi.security.base import SecurityBase

from src.api.common.exceptions import ForbiddenError
from src.cache.core.client import RedisClient
from src.common.dto import Fingerprint, TokensExpire, Status
from src.api.common.providers.stub import Stub
from src.common.dto.user import User
from src.database.gateway import DBGateway
from src.services.security.jwt_token import TokenJWT


TokenType = Literal["access", "refresh"]


class Authorization(SecurityBase):
    def __init__(self, *permissions: Any) -> None:
        self.model = HTTPBearerModel()
        self.scheme_name = type(self).__name__
        self._permission = permissions

    async def __call__(
        self,
        request: Request,
        jwt: Annotated[TokenJWT, Depends(Stub(TokenJWT))],
        database: Annotated[DBGateway, Depends(Stub(DBGateway))],
    ) -> User:
        token = self._get_token(request)
        return await self.verify_token(jwt, database, token, "access")

    async def verify_refresh(
        self,
        body: Fingerprint,
        *,
        request: Request,
        jwt: Annotated[TokenJWT, Depends(Stub(TokenJWT))],
        database: Annotated[DBGateway, Depends(Stub(DBGateway))],
        cache: Annotated[RedisClient, Depends(Stub(RedisClient))],
    ) -> TokensExpire:
        token = request.cookies.get("refresh_token", "")
        user = await self.verify_token(jwt, database, token, "refresh")

        token_pairs = await cache.get_list(str(user.id))
        verified: Optional[str] = None

        for pair in token_pairs:
            data = pair.split("::")
            if len(data) < 2:
                await cache.delete(str(user.id))
                raise ForbiddenError(
                    "Broken separator, try to login again. Token is not valid anymore"
                )
            fp, cached_token, *_ = data
            if fp == body.fingerprint and cached_token == token:
                verified = pair
                break

        if not verified:
            await cache.delete(str(user.id))
            raise ForbiddenError("Token is not valid anymore")

        await cache.pop(str(user.id), verified)
        _, access = await run_in_threadpool(
            jwt.create_jwt_token, type="access", sub=str(user.id)
        )
        expire, refresh = await run_in_threadpool(
            jwt.create_jwt_token, type="refresh", sub=str(user.id)
        )
        await cache.set_list(str(user.id), f"{body.fingerprint}::{refresh.token}")

        return TokensExpire(
            acces_token=access.token, refresh_token=refresh.token, expire_date=expire
        )

    async def verify_token(
        self, jwt: TokenJWT, database: DBGateway, token: str, token_type: TokenType
    ) -> User:
        payload = await run_in_threadpool(jwt.verify_jwt_token, token)
        user_id = payload.get("sub")
        token_type = payload.get("type")

        if token_type != token_type:
            raise ForbiddenError("Invalid token")

        async with database:
            user = await database.user().get_one(user_id=user_id)

        if not user:
            raise ForbiddenError("Not authenticated")

        return user

    def _get_token(self, request: Request) -> str:
        authorization = request.headers.get("authorization")
        scheme, _, token = authorization.partition(" ")
        if not (authorization and scheme and token):
            raise ForbiddenError("Not authenticated")
        if scheme.lower() != "bearer":
            raise ForbiddenError("Invalid authentication credentials")

        return token


class Logout(Authorization):
    async def __call__(
        self,
        request: Request,
        jwt: Annotated[TokenJWT, Depends(Stub(TokenJWT))],
        database: Annotated[DBGateway, Depends(Stub(DBGateway))],
        cache: Annotated[RedisClient, Depends(Stub(RedisClient))],
    ):
        token = self._get_token(request)
        user = await self.verify_token(jwt, database, token, "refresh")

        token_pairs = await cache.get_list(user.id)
        for token in token_pairs:
            data = token.split("::")
            if len(data) < 2:
                await cache.delete(str(user.id))
                break
            _, cached_token, *_ = data
            if cached_token == token:
                await cache.pop(str(user.id), token)
                break

        return Status(ok=True)
