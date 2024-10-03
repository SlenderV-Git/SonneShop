import uuid
from typing import Annotated, Any, Literal, Optional

from fastapi import Depends, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.openapi.models import HTTPBearer as HTTPBearerModel
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param

from src.common.dto.token import Fingerprint
from src.services.security.argon_hasher import Argon2
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
        hasher: Annotated[Argon2, Depends(Stub(Argon2))],
    ) -> User:
        print(request.headers.get("authorization"))
        print(request.cookies)
        print(request.fi)
        return True

    async def verify_refresh(
        self,
        body: Fingerprint,
        *,
        request: Request,
        jwt: Annotated[TokenJWT, Depends(Stub(TokenJWT))],
        database: Annotated[DBGateway, Depends(Stub(DBGateway))],
    ) -> bool:
        return True
