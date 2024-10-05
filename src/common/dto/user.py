from typing import Optional
from pydantic import EmailStr, field_validator

from src.common.dto.base import DTO


class UserSchema(DTO):
    login: str
    email: EmailStr
    password: str

    @field_validator("password")
    def check_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must have at least 8 characters")

        if not any(c.isupper() for c in value):
            raise ValueError("Password must have at least one uppercase letter")

        if not any(c.islower() for c in value):
            raise ValueError("Password must have at least one lowercase letter")

        if not any(c.isdigit() for c in value):
            raise ValueError("Password must have at least one digit")

        return value


class Fingerprint(DTO):
    fingerprint: str


class LoginShema(Fingerprint):
    login: str
    password: str


class User(DTO):
    id: int
    login: str


class SelectUserQuery(DTO):
    id: Optional[int] = None
    login: Optional[str] = None


class UpdateUserQuery(UserSchema):
    id: int
