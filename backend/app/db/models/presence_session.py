from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import DateTime, Enum as SQLEnum, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base
from backend.app.db.enums import PresenceStatus

if TYPE_CHECKING:
    from backend.app.db.models.activity_segment import ActivitySegment


class PresenceSession(Base):
    __tablename__ = "presence_sessions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employee_id: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True, index=True)
    track_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tracks.id"), nullable=True, index=True)
    camera_id: Mapped[int] = mapped_column(ForeignKey("cameras.id"), nullable=False, index=True)
    zone_id: Mapped[Optional[int]] = mapped_column(ForeignKey("zones.id"), nullable=True, index=True)
    first_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    last_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[PresenceStatus] = mapped_column(
        SQLEnum(PresenceStatus, native_enum=False, create_constraint=True, validate_strings=True, length=30),
        default=PresenceStatus.VISIBLE,
        nullable=False,
        index=True,
    )
    duration_seconds: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    activity_segments: Mapped[List[ActivitySegment]] = relationship(
        "ActivitySegment", back_populates="session", cascade="all, delete-orphan"
    )
