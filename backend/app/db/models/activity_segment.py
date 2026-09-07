from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import DateTime, Enum as SQLEnum, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base
from backend.app.db.enums import ActivityState

if TYPE_CHECKING:
    from backend.app.db.models.presence_session import PresenceSession


class ActivitySegment(Base):
    __tablename__ = "activity_segments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("presence_sessions.id"), nullable=False, index=True)
    activity_state: Mapped[ActivityState] = mapped_column(
        SQLEnum(ActivityState, native_enum=False, create_constraint=True, validate_strings=True, length=30),
        nullable=False,
    )
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_seconds: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    session: Mapped[PresenceSession] = relationship("PresenceSession", back_populates="activity_segments")
