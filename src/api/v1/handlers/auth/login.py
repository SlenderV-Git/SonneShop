from typing import Annotated

from fastapi import Depends
from fastapi.concurrency import run_in_threadpool

from src.cache.core.client import RedisClient
from src.common.dto import TokensExpire
from src.common.exceptions.routers import NotFoundException, UnAuthorizedException
from src.api.common.providers.stub import Stub
from src.common.dto.user import LoginShema
from src.database.gateway import DBGateway
from src.services.security.argon_hasher import Argon2
from src.services.security.jwt_token import TokenJWT


class Login:
    async def __call__(
        self,
        login_data: LoginShema,
        jwt: Annotated[TokenJWT, Depends(Stub(TokenJWT))],
        database: Annotated[DBGateway, Depends(Stub(DBGateway))],
        cache: Annotated[RedisClient, Depends(Stub(RedisClient))],
        hasher: Annotated[Argon2, Depends(Stub(Argon2))],
    ) -> TokensExpire:
        user = await database.user().get_one(login=login_data.login)

        if not user:
            raise NotFoundException(f"User {login_data.login} not found")

        if not hasher.verify_password(user.password, login_data.password):
            raise UnAuthorizedException("Incorrect password")

        _, accesss = await run_in_threadpool(
            jwt.create_jwt_token, type="access", sub=str(user.id)
        )
        expire, refresh = await run_in_threadpool(
            jwt.create_jwt_token, type="reflesh", sub=str(user.id)
        )

        tokens = await cache.get_list(str(user.id))
        if len(tokens) > cache.DEFAULT_TOKENS_COUNT:
            await cache.delete(str(user.id))

        await cache.set_list(str(user.id), f"{login_data.fingerprint}::{refresh.token}")
        return TokensExpire(
            acces_token=accesss.token, refresh_token=refresh.token, expire_date=expire
        )
