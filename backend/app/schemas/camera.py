"""Pydantic request and response schemas for camera management and telemetry."""

from __future__ import annotations

from datetime import datetime
import re
from typing import Optional, Set
from urllib.parse import parse_qsl, urlsplit
from pydantic import BaseModel, ConfigDict, Field, model_validator

from backend.app.db.enums import CameraSourceType

_CREDENTIAL_PATTERN = re.compile(r"^[a-zA-Z0-9+.-]+://[^/]*@")
_CREDENTIAL_REF_PATTERN = re.compile(r"^[A-Z0-9_]+$")
_SENSITIVE_QUERY_KEYS: Set[str] = {
    "password",
    "passwd",
    "pwd",
    "token",
    "access_token",
    "auth_token",
    "api_key",
    "apikey",
    "secret",
    "signature",
    "sig",
}


def _validate_clean_rtsp_url(url: Optional[str]) -> Optional[str]:
    """Ensure RTSP URL contains neither inline userinfo nor sensitive query parameters."""
    if url is None:
        return None
    trimmed = url.strip()
    if not trimmed:
        return None

    parsed = urlsplit(trimmed)
    if (
        parsed.username is not None
        or parsed.password is not None
        or "@" in parsed.netloc
        or _CREDENTIAL_PATTERN.search(trimmed) is not None
    ):
        raise ValueError(
            "RTSP URL must not contain embedded credentials or userinfo. "
            "Use credential_ref for camera authentication."
        )

    if parsed.query:
        query_params = parse_qsl(parsed.query, keep_blank_values=True)
        for param_key, _ in query_params:
            cleaned_key = param_key.lower().replace("-", "_")
            if cleaned_key in _SENSITIVE_QUERY_KEYS:
                raise ValueError(
                    "RTSP URL contains a sensitive query parameter. "
                    "Use credential_ref for camera authentication."
                )

    return trimmed


class CameraBase(BaseModel):
    name: str = Field(min_length=1, max_length=100, description="Unique human-readable camera identifier")
    location: Optional[str] = Field(default=None, max_length=150, description="Physical deployment location")
    source_type: CameraSourceType = Field(default=CameraSourceType.RTSP, description="Video source type: WEBCAM or RTSP")
    device_index: Optional[int] = Field(default=None, ge=0, description="OS device index for local USB webcams")
    rtsp_url: Optional[str] = Field(default=None, max_length=255, description="Credential-free RTSP stream URI")
    credential_ref: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Opaque uppercase identifier matching local runtime environment variables",
    )
    target_fps: int = Field(default=5, ge=1, le=30, description="Target processing/inference frame rate")
    reconnect_delay: int = Field(default=5, ge=1, le=60, description="Initial reconnect delay in seconds")


class CameraCreate(CameraBase):
    """Schema for registering a new camera source."""

    @model_validator(mode="after")
    def validate_source_consistency(self) -> CameraCreate:
        # Validate credential reference if provided
        if self.credential_ref is not None:
            clean_ref = self.credential_ref.strip()
            if clean_ref:
                if not _CREDENTIAL_REF_PATTERN.match(clean_ref):
                    raise ValueError(
                        "Invalid credential reference format. Expected uppercase alphanumeric characters and underscores."
                    )
                self.credential_ref = clean_ref
            else:
                self.credential_ref = None

        if self.source_type == CameraSourceType.WEBCAM:
            if self.device_index is None:
                raise ValueError("WEBCAM source type requires a non-null device_index.")
            if self.rtsp_url is not None:
                raise ValueError("WEBCAM source type must not specify an rtsp_url.")
        elif self.source_type == CameraSourceType.RTSP:
            if not self.rtsp_url:
                raise ValueError("RTSP source type requires a non-empty rtsp_url.")
            if self.device_index is not None:
                raise ValueError("RTSP source type must not specify a device_index.")
            self.rtsp_url = _validate_clean_rtsp_url(self.rtsp_url)

        return self


class CameraUpdate(BaseModel):
    """Schema for updating camera configuration."""

    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    location: Optional[str] = Field(default=None, max_length=150)
    source_type: Optional[CameraSourceType] = None
    device_index: Optional[int] = Field(default=None, ge=0)
    rtsp_url: Optional[str] = Field(default=None, max_length=255)
    credential_ref: Optional[str] = Field(default=None, max_length=100)
    is_active: Optional[bool] = None
    target_fps: Optional[int] = Field(default=None, ge=1, le=30)
    reconnect_delay: Optional[int] = Field(default=None, ge=1, le=60)

    @model_validator(mode="after")
    def validate_update(self) -> CameraUpdate:
        if self.credential_ref is not None:
            clean_ref = self.credential_ref.strip()
            if clean_ref:
                if not _CREDENTIAL_REF_PATTERN.match(clean_ref):
                    raise ValueError(
                        "Invalid credential reference format. Expected uppercase alphanumeric characters and underscores."
                    )
                self.credential_ref = clean_ref
            else:
                self.credential_ref = None

        if self.rtsp_url is not None:
            self.rtsp_url = _validate_clean_rtsp_url(self.rtsp_url)

        return self


class CameraResponse(BaseModel):
    """Safe, credential-free camera configuration response."""

    id: int
    name: str
    location: Optional[str]
    source_type: str
    device_index: Optional[int]
    rtsp_url: Optional[str]
    credential_ref: Optional[str]
    is_active: bool
    status: str
    target_fps: int
    reconnect_delay: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class CameraTelemetryResponse(BaseModel):
    """Real-time camera worker telemetry metrics."""

    camera_id: int
    camera_name: str
    source_type: str
    runtime_status: str
    capture_fps: float
    preview_fps: float
    inference_fps: Optional[float] = None
    frames_decoded: int
    frames_published: int
    frames_dropped_or_replaced: int
    last_frame_at: Optional[datetime]
    last_frame_age_ms: Optional[float]
    last_successful_open_at: Optional[datetime]
    last_error_at: Optional[datetime]
    safe_error_code: Optional[str]
    read_failures: int
    reconnect_count: int
    current_backoff_seconds: float
    frame_width: Optional[int]
    frame_height: Optional[int]
    worker_running: bool


class CameraTestProbeResponse(BaseModel):
    """Result of a short-lived connection test probe."""

    success: bool
    source_type: str
    elapsed_ms: float
    camera_id: Optional[int] = None
    frame_width: Optional[int] = None
    frame_height: Optional[int] = None
    safe_error_code: Optional[str] = None
    message: str
