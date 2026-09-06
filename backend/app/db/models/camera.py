from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from backend.app.db.models.zone import Zone

class Camera(Base, TimestampMixin):
    __tablename__ = 'cameras'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    location: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    rtsp_url: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    target_fps: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    reconnect_delay: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default='OFFLINE', nullable=False, index=True)
    zones: Mapped[List[Zone]] = relationship('Zone', back_populates='camera', cascade='all, delete-orphan')
