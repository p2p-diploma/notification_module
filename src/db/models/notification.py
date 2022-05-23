import datetime
import uuid

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped

from db.base_class import Base


class Notification(Base):
    id: Mapped[UUID] = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = Column(String, nullable=False)
    description: Mapped[str] = Column(String, nullable=False)
    owner: Mapped[str] = Column(String, index=True, nullable=False)
    is_read: Mapped[bool] = Column(Boolean(), default=False)
    created_at: Mapped[datetime.datetime] = Column(DateTime, default=datetime.datetime.now())
