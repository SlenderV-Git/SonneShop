from fastapi import FastAPI

from src.api.v1.endpoints import (
    healthcheck_router,
    auth_router,
    user_router,
    payment_router,
)


def init_routers(app: FastAPI) -> None:
    app.include_router(payment_router, prefix="/api/v1/payment")
    app.include_router(user_router, prefix="/api/v1/user")
    app.include_router(auth_router, prefix="/api/v1/auth")
    app.include_router(healthcheck_router, prefix="/api/v1/healthcheck")
