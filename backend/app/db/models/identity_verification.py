from __future__ import annotations
from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from backend.app.db.base import Base

class IdentityVerification(Base):
    __tablename__ = 'identity_verifications'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    track_id: Mapped[int] = mapped_column(ForeignKey('tracks.id'), nullable=False, index=True)
    employee_id: Mapped[Optional[int]] = mapped_column(ForeignKey('employees.id'), nullable=True, index=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    vote_count: Mapped[int] = mapped_column(Integer, nullable=False)
    match_margin: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    verified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
