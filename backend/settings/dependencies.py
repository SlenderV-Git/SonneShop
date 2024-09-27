from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from backend.database.core.connection import create_engine, create_async_session_maker
from backend.database.gateway import DBGateway
from backend.database.core.manager import TransactionManager
from backend.settings.env import DatabaseSettings, JWTSettings, RedisSettings
from backend.security.jwt_token import TokenJWT
from backend.security.bcrypt_hasher import BcryptHasher
from backend.security.pwd_context import get_pwd_context
from backend.database.factory import create_database_factory
from backend.utils.singleton import singleton
from backend.cache.core.client import RedisClient


def init_dependencies(
        app: FastAPI,
        db_settings: DatabaseSettings,
        jwt_settings: JWTSettings,
        redis_settings: RedisSettings
) -> None:
    engine = create_engine(db_settings.get_url_obj)
    session = create_async_session_maker(engine)
    db_factory = create_database_factory(TransactionManager, session)
    redis_client = RedisClient.from_url(redis_settings.get_url)

    jwt_token = TokenJWT(jwt_settings)

    bcrypt_pwd_context = get_pwd_context(['bcrypt'])
    bcrypt_hasher = BcryptHasher(bcrypt_pwd_context)

    app.dependency_overrides[DBGateway] = db_factory
    app.dependency_overrides[TokenJWT] = singleton(jwt_token)
    app.dependency_overrides[BcryptHasher] = singleton(bcrypt_hasher)
    app.dependency_overrides[RedisClient] = singleton(redis_client)
    app.dependency_overrides[RedisSettings] = singleton(redis_settings)