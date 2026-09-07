from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base
from backend.app.db.enums import UnknownResolutionStatus

if TYPE_CHECKING:
    from backend.app.db.models.unknown_event import UnknownEvent


class UnknownPerson(Base):
    __tablename__ = "unknown_people"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    track_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tracks.id"), nullable=True, index=True)
    first_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    last_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    resolution_status: Mapped[UnknownResolutionStatus] = mapped_column(
        SQLEnum(UnknownResolutionStatus, native_enum=False, create_constraint=True, validate_strings=True, length=30),
        default=UnknownResolutionStatus.UNRESOLVED,
        nullable=False,
        index=True,
    )
    events: Mapped[List[UnknownEvent]] = relationship(
        "UnknownEvent", back_populates="unknown_person", cascade="all, delete-orphan"
    )
