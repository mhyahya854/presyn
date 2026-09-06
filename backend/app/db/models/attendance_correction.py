from __future__ import annotations
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.base import Base

if TYPE_CHECKING:
    from backend.app.db.models.attendance_record import AttendanceRecord

class AttendanceCorrection(Base):
    __tablename__ = 'attendance_corrections'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    record_id: Mapped[int] = mapped_column(ForeignKey('attendance_records.id'), nullable=False, index=True)
    admin_user_id: Mapped[int] = mapped_column(ForeignKey('users_admins.id'), nullable=False, index=True)
    original_value: Mapped[str] = mapped_column(Text, nullable=False)
    corrected_value: Mapped[str] = mapped_column(Text, nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    record: Mapped[AttendanceRecord] = relationship('AttendanceRecord', back_populates='corrections')
