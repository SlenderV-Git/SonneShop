from random import randrange

import pytest_asyncio
from faker import Faker

from src.common.dto import ProductSchema
from src.database.gateway import DBGateway
from src.database.models.user import UserModel


@pytest_asyncio.fixture(autouse=True, scope="session", loop_scope="session")
async def accounts(gateway: DBGateway, user: UserModel):
    return [await gateway.account().create(user.id) for _ in range(3)]


@pytest_asyncio.fixture(autouse=True, scope="session", loop_scope="session")
async def products(gateway: DBGateway, faker: Faker):
    products = []

    for _ in range(3):
        product = ProductSchema(
            title=faker.sentence(nb_words=3),
            description=faker.paragraph(nb_sentences=5),
            price=randrange(10, 10000),
        )
        products.append(await gateway.product().create(**product.model_dump()))
    return products
