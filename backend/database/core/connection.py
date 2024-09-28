from typing import Optional
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import URL

from backend.common.types import SessionFactory


def create_engine(url_obj: URL, echo: Optional[bool] = False) -> AsyncEngine:
    return create_async_engine(url_obj, echo=echo)


def create_async_session_maker(engine: AsyncEngine) -> SessionFactory:
    return async_sessionmaker(engine, class_=AsyncSession)
