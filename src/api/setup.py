from typing import Optional

import uvicorn
from fastapi import FastAPI

from src.api.v1.setup import init_v1_routers
from src.api.v1.dependencies import init_dependencies
from src.core.settings import (
    DatabaseSettings,
    JWTSettings,
    RedisSettings,
    DocumentationSettings,
)


def init_app(
    db_settings: DatabaseSettings,
    jwt_settings: JWTSettings,
    redis_settings: RedisSettings,
    doc_settings: DocumentationSettings,
    docs_url: Optional[str] = "/docs",
    redoc_url: Optional[str] = "/redoc",
) -> FastAPI:
    app = FastAPI(
        title=doc_settings.TITLE,
        docs_url=docs_url,
        redoc_url=redoc_url,
        summary=doc_settings.SUMMARY,
        description=doc_settings.DESCRIPTION,
    )
    v1_root_router = init_v1_routers()
    app.include_router(v1_root_router)
    init_dependencies(app, db_settings, jwt_settings, redis_settings)

    return app


def start_app(app: FastAPI, host: str = "0.0.0.0", port: int = 8080) -> None:
    uvicorn.run(app, host=host, port=port)
