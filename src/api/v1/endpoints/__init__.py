from .auth import auth_router
from .healthcheck import healthcheck_router
from .user import user_router
from .payment import payment_router
from .product import product_router
from .warehouse import warehouse_router

__all__ = (
    auth_router,
    healthcheck_router,
    user_router,
    payment_router,
    product_router,
    warehouse_router,
)
