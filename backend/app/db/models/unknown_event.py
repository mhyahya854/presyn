from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.base import Base

if TYPE_CHECKING:
    from backend.app.db.models.unknown_person import UnknownPerson

class UnknownEvent(Base):
    __tablename__ = 'unknown_events'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    unknown_id: Mapped[int] = mapped_column(ForeignKey('unknown_people.id'), nullable=False, index=True)
    camera_id: Mapped[int] = mapped_column(ForeignKey('cameras.id'), nullable=False, index=True)
    zone_id: Mapped[Optional[int]] = mapped_column(ForeignKey('zones.id'), nullable=True, index=True)
    snapshot_path: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    unknown_person: Mapped[UnknownPerson] = relationship('UnknownPerson', back_populates='events')
