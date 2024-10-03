from typing import Literal, Optional, Any, Tuple
from datetime import datetime, timedelta, timezone

from jwt import PyJWTError, encode, decode

from src.common.exceptions.services import ServiceNotImplementedError
from src.core.settings import JWTSettings
from src.common.exceptions import UnAuthorizedException
from src.common.dto import Token

TokenType = Literal["access", "refresh"]


class TokenJWT:
    def __init__(self, settings: JWTSettings) -> None:
        self.settings = settings

    def create_jwt_token(
        self,
        type: TokenType,
        sub: str,
        expires_delta: Optional[timedelta] = None,
        **kw: Any,
    ) -> Tuple[datetime, Token]:
        now = datetime.now(timezone.utc)
        if expires_delta:
            expire = now + expires_delta
        else:
            seconds_delta = (
                self.settings.acces_token_expiration
                if type == "access"
                else self.settings.reflesh_token_expiration
            )
            expire = now + timedelta(seconds=seconds_delta)

        if now >= expire:
            raise ServiceNotImplementedError("Invalid expiration delta was provided")

        to_encode = {
            "exp": expire,
            "sub": sub,
            "iat": now,
            "type": type,
        }
        token = encode(
            to_encode | kw, self.settings.private_key, algorithm=self.settings.algorithm
        )
        return expire, Token(token=token)

    def verify_jwt_token(self, token: str) -> Optional[Any]:
        try:
            decoded_data = decode(
                token, self.settings.public_key, algorithms=[self.settings.algorithm]
            )
            return decoded_data

        except PyJWTError:
            raise UnAuthorizedException("Token is invalid or expired")
