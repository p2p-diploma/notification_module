import datetime
from typing import Optional

from pydantic import BaseModel


class NotificationBase(BaseModel):
    title: Optional[str] = ""
    description: Optional[str] = ""
    owner: Optional[str] = ""
    is_read: Optional[bool]
    created_at: Optional[datetime.datetime]


class NotificationCreate(BaseModel):
    title: str
    description: str
    owner: str


class NotificationUpdate(BaseModel):
    title: str
    description: str


class NotificationInDBBase(NotificationBase):
    class Config:
        orm_mode = True


class Notification(NotificationInDBBase):
    pass
