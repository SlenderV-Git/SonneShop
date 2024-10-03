from typing import Literal, Optional
from fastapi import FastAPI

from src.services.gateway import ServicesGateway
from src.api.common.mediator.mediator import CommandMediator
from src.services.factory import create_service_gateway_factory
from src.database.core import (
    create_engine,
    create_async_session_maker,
    TransactionManager,
)
from src.database.gateway import DBGateway
from src.core.settings import DatabaseSettings, JWTSettings, RedisSettings
from src.services.security import TokenJWT, Argon2, get_argon2_hasher
from src.database.factory import create_database_factory
from src.common.tools import singleton
from src.cache.core.client import RedisClient


APP_STATUS = Literal["test", "production"]


def init_dependencies(
    app: FastAPI,
    db_settings: DatabaseSettings,
    jwt_settings: JWTSettings,
    redis_settings: RedisSettings,
    app_status: Optional[APP_STATUS] = "production",
) -> None:
    engine = create_engine(
        db_settings.get_url_obj if app_status == "production" else db_settings.TEST_HOST
    )
    session = create_async_session_maker(engine)
    db_factory = create_database_factory(TransactionManager, session)
    service_factory = create_service_gateway_factory(db_factory)
    hasher = get_argon2_hasher()

    redis_client = RedisClient.from_url(redis_settings.get_url)
    jwt_token = TokenJWT(jwt_settings)

    mediator = CommandMediator()
    mediator.setup(
        engine=engine,
        session=session,
        db_gateway=db_factory,
        service_gateway=service_factory,
        redis_client=redis_client,
        jwt_token=jwt_token,
        hasher=hasher,
    )

    app.dependency_overrides[CommandMediator] = mediator
    app.dependency_overrides[ServicesGateway] = service_factory
    app.dependency_overrides[DBGateway] = db_factory
    app.dependency_overrides[TokenJWT] = singleton(jwt_token)
    app.dependency_overrides[Argon2] = singleton(hasher)
    app.dependency_overrides[RedisClient] = singleton(redis_client)
    app.dependency_overrides[RedisSettings] = singleton(redis_settings)
