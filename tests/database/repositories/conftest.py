from random import randrange

import pytest
import pytest_asyncio
from faker import Faker

from backend.common.dto import UserSchema, ProductSchema
from backend.database.gateway import DBGateway
from backend.database.models.user import UserModel


@pytest.fixture(autouse=True, scope="session")
def user_dto(faker : Faker):
    return UserSchema(
        login = faker.name(),
        email = faker.email(safe=True),
        password = faker.password(length=10)
    )
    
@pytest_asyncio.fixture(autouse=True, scope="session", loop_scope="session")
async def user(gateway: DBGateway, user_dto : UserSchema):
    await gateway.user().create(**user_dto.model_dump())
    return await gateway.user().get_one(login=user_dto.login)

@pytest_asyncio.fixture(autouse=True, scope="session", loop_scope="session")
async def accounts(gateway: DBGateway, user : UserModel):
    return [await gateway.account().create(user.id) for _ in range(3)]


@pytest_asyncio.fixture(autouse=True, scope="session", loop_scope="session")
async def products(gateway: DBGateway, faker : Faker):
    products = []

    for _ in range(3):
        product = ProductSchema(
            title = faker.sentence(nb_words=3),
            description = faker.paragraph(nb_sentences=5),
            price = randrange(10, 10000) 
        )
        products.append(
            await gateway.product().create(**product.model_dump())
        )
    return products
