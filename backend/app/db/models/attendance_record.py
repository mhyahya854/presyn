from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from backend.app.db.models.employee import Employee
    from backend.app.db.models.attendance_correction import AttendanceCorrection

class AttendanceRecord(Base, TimestampMixin):
    __tablename__ = 'attendance_records'
    __table_args__ = (UniqueConstraint('employee_id', 'date', name='uq_employee_attendance_date'),)
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey('employees.id'), nullable=False, index=True)
    date: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    arrival_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    departure_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(30), default='PRESENT', nullable=False)
    employee: Mapped[Employee] = relationship('Employee', back_populates='attendance_records')
    corrections: Mapped[List[AttendanceCorrection]] = relationship('AttendanceCorrection', back_populates='record', cascade='all, delete-orphan')
