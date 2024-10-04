from faker import Faker
import pytest
from src.api.common.mediator.mediator import CommandMediator
from src.common.dto.user import User, UserSchema
from src.services.security.argon_hasher import Argon2


class TestMediator:
    @pytest.mark.asyncio
    async def test_command_create_user(
        self, mediator: CommandMediator, hasher: Argon2, faker: Faker
    ):
        user_schema = UserSchema(
            login=faker.name(), email=faker.email(), password=faker.password()
        )
        user: User = await mediator.send(user_schema, hasher=hasher)

        assert user.login == user_schema.login
