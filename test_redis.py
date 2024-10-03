import asyncio
from pydantic import BaseModel
from src.cache.core.client import RedisClient
from fakeredis.aioredis import FakeRedis


client = RedisClient(client=FakeRedis())


class User(BaseModel):
    user_id: str
    login: str
    access_token: str


user = User(user_id="1", login="Victor", access_token="hello")


async def main():
    print(await client.set_dict(user.user_id, user.model_dump()))
    print(await client.get_dict_all(user.user_id))


asyncio.run(main())
