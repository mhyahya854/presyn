"""Thread-safe real runtime telemetry state collector for active cameras."""

from __future__ import annotations

from collections import deque
from datetime import datetime, timezone
import threading
import time
from typing import Deque, Optional

from backend.app.camera.types import CameraTelemetryState


class CameraTelemetryCollector:
    """In-memory telemetry accumulator for a single camera worker."""

    def __init__(self, camera_id: int, camera_name: str, source_type: str) -> None:
        self.camera_id = camera_id
        self.camera_name = camera_name
        self.source_type = source_type

        self._lock = threading.Lock()
        self._runtime_status: str = "OFFLINE"
        self._worker_running: bool = False

        self._frames_decoded: int = 0
        self._frames_published: int = 0
        self._frames_dropped_or_replaced: int = 0

        self._last_frame_at: Optional[datetime] = None
        self._last_successful_open_at: Optional[datetime] = None
        self._last_error_at: Optional[datetime] = None
        self._safe_error_code: Optional[str] = None

        self._read_failures: int = 0
        self._reconnect_count: int = 0
        self._current_backoff_seconds: float = 0.0

        self._frame_width: Optional[int] = None
        self._frame_height: Optional[int] = None

        # Rolling window of monotonic timestamps for measured FPS calculation
        self._capture_timestamps: Deque[float] = deque(maxlen=60)
        self._preview_timestamps: Deque[float] = deque(maxlen=60)

    def set_worker_running(self, running: bool) -> None:
        with self._lock:
            self._worker_running = running

    def set_status(self, status: str) -> None:
        with self._lock:
            self._runtime_status = status

    def record_successful_open(self) -> None:
        now = datetime.now(timezone.utc)
        with self._lock:
            self._last_successful_open_at = now
            self._read_failures = 0
            self._safe_error_code = None

    def record_frame_decoded(self, width: int, height: int) -> None:
        now_utc = datetime.now(timezone.utc)
        now_mono = time.monotonic()
        with self._lock:
            self._frames_decoded += 1
            self._last_frame_at = now_utc
            self._frame_width = width
            self._frame_height = height
            self._read_failures = 0
            self._capture_timestamps.append(now_mono)

    def record_preview_published(self) -> None:
        now_mono = time.monotonic()
        with self._lock:
            self._frames_published += 1
            self._preview_timestamps.append(now_mono)

    def record_frame_replaced(self) -> None:
        with self._lock:
            self._frames_dropped_or_replaced += 1

    def record_read_failure(self, error_code: str = "READ_FRAME_FAILED") -> None:
        now = datetime.now(timezone.utc)
        with self._lock:
            self._read_failures += 1
            self._last_error_at = now
            self._safe_error_code = error_code

    def record_reconnect_attempt(self, backoff_seconds: float) -> None:
        now = datetime.now(timezone.utc)
        with self._lock:
            self._reconnect_count += 1
            self._current_backoff_seconds = backoff_seconds
            self._last_error_at = now

    def reset_backoff(self) -> None:
        with self._lock:
            self._current_backoff_seconds = 0.0

    def _calculate_fps(self, timestamps: Deque[float]) -> float:
        if len(timestamps) < 2:
            return 0.0
        duration = timestamps[-1] - timestamps[0]
        if duration <= 0:
            return 0.0
        # If the most recent frame is older than 2.0s, FPS has effectively stalled
        if (time.monotonic() - timestamps[-1]) > 2.0:
            return 0.0
        return round((len(timestamps) - 1) / duration, 1)

    def get_snapshot(self) -> CameraTelemetryState:
        """Return a point-in-time truthful telemetry snapshot without holding locks during caller usage."""
        now_utc = datetime.now(timezone.utc)
        with self._lock:
            capture_fps = self._calculate_fps(self._capture_timestamps)
            preview_fps = self._calculate_fps(self._preview_timestamps)

            last_age_ms: Optional[float] = None
            if self._last_frame_at is not None:
                last_age_ms = max(0.0, round((now_utc - self._last_frame_at).total_seconds() * 1000, 1))

            return CameraTelemetryState(
                camera_id=self.camera_id,
                camera_name=self.camera_name,
                source_type=self.source_type,
                runtime_status=self._runtime_status,
                capture_fps=capture_fps,
                preview_fps=preview_fps,
                inference_fps=None,  # Truthfully None in Phase 02
                frames_decoded=self._frames_decoded,
                frames_published=self._frames_published,
                frames_dropped_or_replaced=self._frames_dropped_or_replaced,
                last_frame_at=self._last_frame_at,
                last_frame_age_ms=last_age_ms,
                last_successful_open_at=self._last_successful_open_at,
                last_error_at=self._last_error_at,
                safe_error_code=self._safe_error_code,
                read_failures=self._read_failures,
                reconnect_count=self._reconnect_count,
                current_backoff_seconds=self._current_backoff_seconds,
                frame_width=self._frame_width,
                frame_height=self._frame_height,
                worker_running=self._worker_running,
            )
