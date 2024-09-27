import pytest
import pytest_asyncio
from backend.common.dto.user import UserSchema
from backend.database.gateway import DBGateway
from backend.database.models.user import UserModel

@pytest.fixture(autouse=True, scope="session")
def user_dto():
    return UserSchema(
        login = "Victor",
        email = "example@gmail.com",
        password = "H2aaddMMSNASK4"
    )
    
@pytest_asyncio.fixture(autouse=True, scope="session", loop_scope="session")
async def user(gateway: DBGateway, user_dto : UserSchema):
    await gateway.user().create(**user_dto.model_dump())
    return await gateway.user().get_one(login=user_dto.login)

@pytest_asyncio.fixture(autouse=True, scope="session", loop_scope="session")
async def accounts(gateway: DBGateway, user : UserModel):
    return [await gateway.account().create(user.id) for _ in range(3)]


