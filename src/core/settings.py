from logging import Formatter
from pathlib import Path
from typing import Final

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import DirectoryPath
from sqlalchemy import URL


def get_root_dir_path() -> Path:
    return Path(__file__).resolve().parent.parent.parent


class DatabaseSettings(BaseSettings):
    root_dir_path: DirectoryPath = get_root_dir_path()
    model_config = SettingsConfigDict(
        env_file=f"{root_dir_path}/.env",
        env_file_encoding="utf-8",
        env_prefix="POSTGRES_",
        extra="ignore",
    )
    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    DB: str
    TEST_HOST: Final[str] = "sqlite+aiosqlite:///example.db"

    @property
    def get_url_obj(self) -> URL:
        return URL.create(
            "postgresql+asyncpg",
            username=self.USER,
            password=self.PASSWORD,
            database=self.DB,
            host=self.HOST,
            port=self.PORT,
        )

    @property
    def get_url_str(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.USER}:"
            f"{self.PASSWORD}@"
            f"{self.HOST}:"
            f"{self.PORT}/"
            f"{self.DB}"
        )


class JWTSettings:
    private_key: Final[str] = (
        get_root_dir_path() / ".certs" / "jwt_private.pem"
    ).read_text()

    public_key: Final[str] = (
        get_root_dir_path() / ".certs" / "jwt_public.pem"
    ).read_text()

    algorithm: Final[str] = "RS256"
    acces_token_expiration: Final[int] = 3000
    reflesh_token_expiration: Final[int] = 9000


class SignatureSettings:
    private_key: Final[bytes] = (
        get_root_dir_path() / ".certs" / "signature_private.pem"
    ).read_text()


class RedisSettings(BaseSettings):
    root_dir_path: DirectoryPath = get_root_dir_path()
    model_config = SettingsConfigDict(
        env_file=f"{root_dir_path}/.env",
        env_file_encoding="utf-8",
        env_prefix="REDIS_",
        extra="ignore",
    )

    HOST: str
    PORT: int
    PASSWORD: str

    @property
    def get_url(self) -> str:
        return f"redis://{self.HOST}:{self.PORT}"


class ElasticSettings(BaseSettings):
    root_dir_path: DirectoryPath = get_root_dir_path()
    model_config = SettingsConfigDict(
        env_file=f"{root_dir_path}/.env",
        env_file_encoding="utf-8",
        env_prefix="ELASTIC_",
        extra="ignore",
    )

    HOST: str
    PORT: int
    PASSWORD: str
    LOG_INDEX: str


class LoggerSettings:
    formatter: Final[Formatter] = Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s\n"
    )


class DocumentationSettings(BaseSettings):
    root_dir_path: DirectoryPath = get_root_dir_path()
    model_config = SettingsConfigDict(
        env_file=f"{root_dir_path}/.env",
        env_file_encoding="utf-8",
        env_prefix="DOC_",
        extra="ignore",
    )
    TITLE: str
    DESCRIPTION: str
    SUMMARY: str


def get_db_settings() -> DatabaseSettings:
    return DatabaseSettings()


def get_jwt_settings() -> JWTSettings:
    return JWTSettings()


def get_redis_settings() -> RedisSettings:
    return RedisSettings()


def get_signature_settings() -> SignatureSettings:
    return SignatureSettings()


def get_elastic_settings() -> ElasticSettings:
    return ElasticSettings()


def get_documentation_settings() -> DocumentationSettings:
    return DocumentationSettings()
