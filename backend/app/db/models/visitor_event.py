from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.base import Base

if TYPE_CHECKING:
    from backend.app.db.models.visitor import Visitor

class VisitorEvent(Base):
    __tablename__ = 'visitor_events'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    visitor_id: Mapped[int] = mapped_column(ForeignKey('visitors.id'), nullable=False, index=True)
    camera_id: Mapped[int] = mapped_column(ForeignKey('cameras.id'), nullable=False, index=True)
    zone_id: Mapped[Optional[int]] = mapped_column(ForeignKey('zones.id'), nullable=True, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    visitor: Mapped[Visitor] = relationship('Visitor', back_populates='events')
