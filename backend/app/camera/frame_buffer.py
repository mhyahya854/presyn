"""Thread-safe, bounded latest-frame buffer preventing latency accumulation."""

from __future__ import annotations

import threading
from typing import Optional

from backend.app.camera.types import EncodedPreviewFrame, RawFrame


class LatestFrameBuffer:
    """Thread-safe latest-frame storage with bounded depth 1.

    Ownership Model:
    - The capture thread produces and writes RawFrame instances to the buffer.
    - When a new frame arrives before the previous frame is consumed, the previous frame is dropped/replaced.
    - Consumers that may mutate the frame data (e.g. CV inference, drawing overlays) request a defensive copy.
    - Locks are held strictly for pointer assignment and reading references; never during encoding or network I/O.
    """

    def __init__(self, camera_id: int) -> None:
        self.camera_id = camera_id
        self._lock = threading.Lock()
        self._latest_raw: Optional[RawFrame] = None
        self._latest_preview: Optional[EncodedPreviewFrame] = None
        self._total_replaced: int = 0

    def update_raw(self, frame: RawFrame) -> None:
        """Store the newly arrived raw frame, replacing any stale frame."""
        with self._lock:
            if self._latest_raw is not None:
                self._total_replaced += 1
            self._latest_raw = frame

    def get_latest_raw(self, copy: bool = False) -> Optional[RawFrame]:
        """Retrieve the latest raw frame. If copy is True, return a deep copy of the NumPy array."""
        with self._lock:
            frame = self._latest_raw

        if frame is None:
            return None

        if copy:
            return RawFrame(
                frame_id=frame.frame_id,
                camera_id=frame.camera_id,
                captured_at=frame.captured_at,
                monotonic_timestamp=frame.monotonic_timestamp,
                width=frame.width,
                height=frame.height,
                data=frame.data.copy(),
            )
        return frame

    def update_preview(self, preview: EncodedPreviewFrame) -> None:
        """Store the latest JPEG-encoded preview frame."""
        with self._lock:
            self._latest_preview = preview

    def get_latest_preview(self) -> Optional[EncodedPreviewFrame]:
        """Retrieve the latest JPEG preview frame. Bytes objects are immutable."""
        with self._lock:
            return self._latest_preview

    def clear(self) -> None:
        """Clear all stored frame references upon worker shutdown."""
        with self._lock:
            self._latest_raw = None
            self._latest_preview = None

    @property
    def total_replaced(self) -> int:
        with self._lock:
            return self._total_replaced
