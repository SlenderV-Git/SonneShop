from pydantic import EmailStr, BaseModel, field_validator


class UserSchema(BaseModel):
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
