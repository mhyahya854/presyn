from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from backend.app.db.models.camera import Camera

class Zone(Base, TimestampMixin):
    __tablename__ = 'zones'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    camera_id: Mapped[int] = mapped_column(ForeignKey('cameras.id'), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    polygon_json: Mapped[str] = mapped_column(Text, nullable=False)
    zone_type: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    camera: Mapped[Camera] = relationship('Camera', back_populates='zones')
