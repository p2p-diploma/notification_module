from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import crud
from core import dependencies
from schemas import Notification

router = APIRouter()


@router.get("/{offset}", response_model=list[Notification])
async def get_notifications(
    *,
    offset: int = 0,
    db: AsyncSession = Depends(dependencies.get_session),
    current_user: dict[str, Any] = Depends(dependencies.get_current_user),
):
    email = current_user['user_id']
    notifications = await crud.notifications.get_multi_by_email(db=db, owner=email, skip=offset)
    return notifications
