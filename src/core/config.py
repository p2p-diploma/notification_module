from typing import Any, Dict, Optional

from pydantic import AnyUrl, BaseSettings, PostgresDsn, validator


class AsyncPostgresDsn(PostgresDsn):
    allowed_schemes = {"postgres+asyncpg", "postgresql+asyncpg"}


class AppSettings(BaseSettings):
    class Config:
        env_file = ".env"

    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI_ASYNC: Optional[AsyncPostgresDsn] = None

    REDIS_HOST: str
    IS_CONSUMER: bool = False

    @validator("POSTGRES_DB", pre=True)
    def assemble_db_name(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if values.get("TEST_MODE"):
            return "postgres"
        if isinstance(v, str):
            return v

    @validator("SQLALCHEMY_DATABASE_URI_ASYNC", pre=True)
    def assemble_async_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return AsyncPostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )


app_settings = AppSettings()