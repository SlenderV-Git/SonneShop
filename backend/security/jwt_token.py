from typing import Optional, Any
from datetime import datetime, timedelta

from jwt import PyJWTError, encode, decode

from backend.settings.env import JWTSettings
from backend.common.exceptions import UnAuthorizedException


class TokenJWT:
    def __init__(self, settings: JWTSettings) -> None:
        self.settings = settings

    def create_jwt_token(self, data: dict) -> str:
        expiration = datetime.now() + timedelta(minutes=self.settings.jwt_expiration)
        data.update({"exp": expiration})
        token = encode(
            data, self.settings.private_key, algorithm=self.settings.algorithm
        )
        return token

    def verify_jwt_token(self, token: str) -> Optional[Any]:
        try:
            decoded_data = decode(
                token, self.settings.public_key, algorithms=[self.settings.algorithm]
            )
            return decoded_data

        except PyJWTError:
            raise UnAuthorizedException("Token is invalid or expired")
