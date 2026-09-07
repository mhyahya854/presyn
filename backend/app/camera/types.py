"""Runtime dataclasses and protocol types for the camera subsystem."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import numpy as np


@dataclass
class RawFrame:
    """In-memory representation of a captured raw video frame."""

    frame_id: int
    camera_id: int
    captured_at: datetime
    monotonic_timestamp: float
    width: int
    height: int
    data: np.ndarray


@dataclass
class EncodedPreviewFrame:
    """In-memory representation of a JPEG-compressed live preview frame."""

    frame_id: int
    camera_id: int
    encoded_at: datetime
    sequence: int
    jpeg_bytes: bytes
    width: int
    height: int


@dataclass
class CameraTelemetryState:
    """Real-time, in-memory telemetry state for an active camera worker."""

    camera_id: int
    camera_name: str
    source_type: str
    runtime_status: str
    capture_fps: float = 0.0
    preview_fps: float = 0.0
    inference_fps: Optional[float] = None  # None in Phase 02 (inference not implemented)
    frames_decoded: int = 0
    frames_published: int = 0
    frames_dropped_or_replaced: int = 0
    last_frame_at: Optional[datetime] = None
    last_frame_age_ms: Optional[float] = None
    last_successful_open_at: Optional[datetime] = None
    last_error_at: Optional[datetime] = None
    safe_error_code: Optional[str] = None
    read_failures: int = 0
    reconnect_count: int = 0
    current_backoff_seconds: float = 0.0
    frame_width: Optional[int] = None
    frame_height: Optional[int] = None
    worker_running: bool = False


@dataclass
class CameraTestResult:
    """Result of a short-lived camera connection probe."""

    success: bool
    source_type: str
    elapsed_ms: float
    camera_id: Optional[int] = None
    frame_width: Optional[int] = None
    frame_height: Optional[int] = None
    safe_error_code: Optional[str] = None
    message: str = ""
