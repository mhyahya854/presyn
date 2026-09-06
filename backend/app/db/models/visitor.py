from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from backend.app.db.models.visitor_event import VisitorEvent

class Visitor(Base, TimestampMixin):
    __tablename__ = 'visitors'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    host_employee_id: Mapped[Optional[int]] = mapped_column(ForeignKey('employees.id'), nullable=True, index=True)
    badge_number: Mapped[Optional[str]] = mapped_column(String(50), unique=True, nullable=True, index=True)
    status: Mapped[str] = mapped_column(String(30), default='EXPECTED', nullable=False, index=True)
    events: Mapped[List[VisitorEvent]] = relationship('VisitorEvent', back_populates='visitor', cascade='all, delete-orphan')
