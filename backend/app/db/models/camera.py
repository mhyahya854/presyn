from __future__ import annotations

import re
from typing import TYPE_CHECKING, List, Optional
from urllib.parse import urlsplit

from sqlalchemy import Boolean, CheckConstraint, Enum as SQLEnum, Integer, String, event
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from backend.app.db.base import Base, TimestampMixin
from backend.app.db.enums import CameraSourceType, CameraStatus

if TYPE_CHECKING:
    from backend.app.db.models.zone import Zone

_CREDENTIAL_PATTERN = re.compile(r"^[a-zA-Z0-9+.-]+://[^/]*@")


class Camera(Base, TimestampMixin):
    __tablename__ = "cameras"
    __table_args__ = (
        CheckConstraint(
            "((source_type = 'WEBCAM' AND device_index IS NOT NULL AND rtsp_url IS NULL) OR "
            "(source_type = 'RTSP' AND device_index IS NULL AND rtsp_url IS NOT NULL))",
            name="chk_camera_source_consistency",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    location: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    source_type: Mapped[CameraSourceType] = mapped_column(
        SQLEnum(CameraSourceType, native_enum=False, create_constraint=True, validate_strings=True, length=20),
        default=CameraSourceType.RTSP,
        nullable=False,
    )
    device_index: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    rtsp_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    credential_ref: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    target_fps: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    reconnect_delay: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    status: Mapped[CameraStatus] = mapped_column(
        SQLEnum(CameraStatus, native_enum=False, create_constraint=True, validate_strings=True, length=20),
        default=CameraStatus.OFFLINE,
        nullable=False,
        index=True,
    )
    zones: Mapped[List[Zone]] = relationship("Zone", back_populates="camera", cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        if "source_type" not in kwargs:
            kwargs["source_type"] = CameraSourceType.RTSP
        super().__init__(**kwargs)
        self.validate_consistency()

    @validates("rtsp_url")
    def validate_rtsp_url(self, key: str, value: Optional[str]) -> Optional[str]:
        if value is not None:
            parsed = urlsplit(value)
            if (
                parsed.username is not None
                or parsed.password is not None
                or "@" in parsed.netloc
                or _CREDENTIAL_PATTERN.search(value) is not None
            ):
                raise ValueError(
                    "RTSP URL must not contain embedded credentials or userinfo. "
                    "Use credential_ref for camera authentication."
                )
        return value

    def validate_consistency(self) -> None:
        source_val = self.source_type.value if isinstance(self.source_type, CameraSourceType) else self.source_type
        if source_val == CameraSourceType.WEBCAM.value:
            if self.device_index is None:
                raise ValueError("WEBCAM camera source requires a non-null device_index.")
            if self.rtsp_url is not None:
                raise ValueError("WEBCAM camera source must have a null rtsp_url.")
        elif source_val == CameraSourceType.RTSP.value:
            if self.rtsp_url is None:
                raise ValueError("RTSP camera source requires a non-null rtsp_url.")
            if self.device_index is not None:
                raise ValueError("RTSP camera source must have a null device_index.")


@event.listens_for(Camera, "before_insert")
@event.listens_for(Camera, "before_update")
def check_camera_consistency_listener(mapper, connection, target: Camera) -> None:
    target.validate_consistency()
