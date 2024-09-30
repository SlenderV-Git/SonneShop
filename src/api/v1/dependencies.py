from fastapi import FastAPI

from src.database.core import (
    create_engine,
    create_async_session_maker,
    TransactionManager,
)
from src.database.gateway import DBGateway
from src.settings.env import DatabaseSettings, JWTSettings, RedisSettings
from src.security import TokenJWT, BcryptHasher, get_pwd_context
from src.database.factory import create_database_factory
from src.common.tools import singleton
from src.cache.core.client import RedisClient


def init_dependencies(
    app: FastAPI,
    db_settings: DatabaseSettings,
    jwt_settings: JWTSettings,
    redis_settings: RedisSettings,
) -> None:
    engine = create_engine(db_settings.get_url_obj)
    session = create_async_session_maker(engine)
    db_factory = create_database_factory(TransactionManager, session)

    redis_client = RedisClient.from_url(redis_settings.get_url)
    jwt_token = TokenJWT(jwt_settings)

    bcrypt_pwd_context = get_pwd_context(["bcrypt"])
    bcrypt_hasher = BcryptHasher(bcrypt_pwd_context)

    app.dependency_overrides[DBGateway] = db_factory
    app.dependency_overrides[TokenJWT] = singleton(jwt_token)
    app.dependency_overrides[BcryptHasher] = singleton(bcrypt_hasher)
    app.dependency_overrides[RedisClient] = singleton(redis_client)
    app.dependency_overrides[RedisSettings] = singleton(redis_settings)
