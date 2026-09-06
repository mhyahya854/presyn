from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from backend.app.db.models.department import Department
    from backend.app.db.models.face_template import FaceTemplate
    from backend.app.db.models.attendance_record import AttendanceRecord

class Employee(Base, TimestampMixin):
    __tablename__ = 'employees'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey('departments.id'), nullable=True, index=True)
    employee_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    job_title: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default='ACTIVE', nullable=False, index=True)
    enrollment_status: Mapped[str] = mapped_column(String(30), default='PENDING', nullable=False)
    department: Mapped[Optional[Department]] = relationship('Department', back_populates='employees')
    face_templates: Mapped[List[FaceTemplate]] = relationship('FaceTemplate', back_populates='employee', cascade='all, delete-orphan')
    attendance_records: Mapped[List[AttendanceRecord]] = relationship('AttendanceRecord', back_populates='employee')
