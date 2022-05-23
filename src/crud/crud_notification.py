from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from db.models import Notification
from schemas.notification import NotificationCreate, NotificationUpdate


class CRUDNotification(CRUDBase[Notification, NotificationCreate, NotificationUpdate]):
    async def get_multi_by_email(
        self, db: AsyncSession, *, owner: str, skip: int = 0, limit: int = 10
    ) -> list[Notification]:
        query = select(self.model).filter(self.model.owner == owner).offset(skip).limit(limit)
        result = await db.execute(query)
        res = result.scalars().all()
        return res


notifications = CRUDNotification(Notification)
