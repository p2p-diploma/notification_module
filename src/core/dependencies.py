from functools import lru_cache
from typing import Any, AsyncGenerator

import jwt
from fastapi import HTTPException
from redis import asyncio as aioredis
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request

from core.config import app_settings
from core.configs import redis_client
from db.session import async_session


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


def get_current_user(request: Request) -> dict[str, Any]:
    unauthorized_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    raw_jwt = request.cookies.get("jwt-access")

    if raw_jwt is None:
        raise unauthorized_exc
    try:
        payload = jwt.decode(
            raw_jwt,
            app_settings.SECRET_KEY,
            algorithms=["HS256"],
        )
    except jwt.PyJWTError as e:
        raise unauthorized_exc from e

    return payload


@lru_cache
def get_redis() -> aioredis.Redis:  # type: ignore
    return redis_client
