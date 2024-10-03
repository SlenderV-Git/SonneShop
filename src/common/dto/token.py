from datetime import datetime
from src.common.dto.base import DTO


class Token(DTO):
    token: str


class Tokens(DTO):
    acces_token: str
    reflesh_token: str


class TokensExpire(Tokens):
    expire_date: datetime
