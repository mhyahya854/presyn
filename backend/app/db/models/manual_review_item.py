from __future__ import annotations
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from backend.app.db.base import Base

class ManualReviewItem(Base):
    __tablename__ = 'manual_review_items'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    item_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    camera_id: Mapped[Optional[int]] = mapped_column(ForeignKey('cameras.id'), nullable=True, index=True)
    candidate_data_json: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default='PENDING', nullable=False, index=True)
    reviewer_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users_admins.id'), nullable=True, index=True)
    resolution_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
