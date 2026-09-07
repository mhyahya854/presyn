"""Injectable video capture adapter boundary for OpenCV webcam and RTSP streams."""

from __future__ import annotations

import sys
from typing import Callable, Optional, Protocol, Tuple, Union
import cv2
import numpy as np

from backend.app.core.logging import logger

# Restrict OpenCV internal native logging to avoid printing stream details
if hasattr(cv2, "setLogLevel"):
    try:
        cv2.setLogLevel(cv2.LOG_LEVEL_ERROR)
    except Exception:
        pass


class VideoCaptureAdapter(Protocol):
    """Abstract protocol for video frame capture sources."""

    def open(self, source: Union[int, str]) -> bool:
        """Open the video stream or device index. Return True on success."""
        ...

    def is_opened(self) -> bool:
        """Check if the capture device is open."""
        ...

    def read(self) -> Tuple[bool, Optional[np.ndarray]]:
        """Read the next frame. Return (success, frame_data)."""
        ...

    def release(self) -> None:
        """Release underlying hardware and stream handles."""
        ...


class OpenCVCaptureAdapter:
    """Production capture adapter utilizing OpenCV VideoCapture with platform optimizations."""

    def __init__(self, source_type: str = "RTSP", timeout_ms: int = 5000) -> None:
        self.source_type = source_type.upper()
        self.timeout_ms = timeout_ms
        self._cap: Optional[cv2.VideoCapture] = None
        self._is_opened: bool = False

    def open(self, source: Union[int, str]) -> bool:
        """Open capture source using platform-recommended backend without leaking source string."""
        self.release()

        try:
            if "WEBCAM" in self.source_type:
                device_idx = int(source)
                # On Windows, prefer DirectShow (cv2.CAP_DSHOW) for faster initialization
                if sys.platform == "win32" and hasattr(cv2, "CAP_DSHOW"):
                    cap = cv2.VideoCapture(device_idx, cv2.CAP_DSHOW)
                    if not cap.isOpened():
                        cap.release()
                        cap = cv2.VideoCapture(device_idx)
                elif sys.platform.startswith("linux") and hasattr(cv2, "CAP_V4L2"):
                    cap = cv2.VideoCapture(device_idx, cv2.CAP_V4L2)
                else:
                    cap = cv2.VideoCapture(device_idx)
            else:
                # RTSP stream: prefer FFmpeg backend where available
                rtsp_src = str(source)
                if hasattr(cv2, "CAP_FFMPEG"):
                    cap = cv2.VideoCapture(rtsp_src, cv2.CAP_FFMPEG)
                else:
                    cap = cv2.VideoCapture(rtsp_src)

            if cap is not None and cap.isOpened():
                # Apply timeout properties if supported by the installed OpenCV build
                if hasattr(cv2, "CAP_PROP_OPEN_TIMEOUT_MSEC"):
                    cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, float(self.timeout_ms))
                if hasattr(cv2, "CAP_PROP_READ_TIMEOUT_MSEC"):
                    cap.set(cv2.CAP_PROP_READ_TIMEOUT_MSEC, float(self.timeout_ms))
                # Set capture buffer to 1 frame to prevent stale frame accumulation in native buffer
                if hasattr(cv2, "CAP_PROP_BUFFERSIZE"):
                    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

                self._cap = cap
                self._is_opened = True
                return True
            else:
                if cap is not None:
                    cap.release()
                self._cap = None
                self._is_opened = False
                return False

        except Exception:
            # Strictly do not log the source string (which might contain credentials)
            logger.warning("Failed to open capture device for source_type=%s", self.source_type)
            self.release()
            return False

    def is_opened(self) -> bool:
        return self._is_opened and self._cap is not None and self._cap.isOpened()

    def read(self) -> Tuple[bool, Optional[np.ndarray]]:
        if not self.is_opened():
            return False, None
        try:
            ret, frame = self._cap.read()  # type: ignore[union-attr]
            if ret and frame is not None and frame.size > 0:
                return True, frame
            return False, None
        except Exception:
            return False, None

    def release(self) -> None:
        if self._cap is not None:
            try:
                self._cap.release()
            except Exception:
                pass
            self._cap = None
        self._is_opened = False


class FakeCaptureAdapter:
    """Deterministic synthetic capture adapter for automated unit and integration tests."""

    def __init__(
        self,
        can_open: bool = True,
        frame_width: int = 640,
        frame_height: int = 480,
        max_reads: Optional[int] = None,
        fail_after_reads: Optional[int] = None,
        exception_on_open: Optional[Exception] = None,
    ) -> None:
        self.can_open = can_open
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.max_reads = max_reads
        self.fail_after_reads = fail_after_reads
        self.exception_on_open = exception_on_open
        self.read_count: int = 0
        self.released: bool = False
        self._opened: bool = False

    def open(self, source: Union[int, str]) -> bool:
        if self.exception_on_open is not None:
            raise self.exception_on_open
        self._opened = self.can_open
        self.released = False
        return self._opened

    def is_opened(self) -> bool:
        return self._opened and not self.released

    def read(self) -> Tuple[bool, Optional[np.ndarray]]:
        if not self.is_opened():
            return False, None

        if self.fail_after_reads is not None and self.read_count >= self.fail_after_reads:
            return False, None

        if self.max_reads is not None and self.read_count >= self.max_reads:
            return False, None

        self.read_count += 1
        # Generate synthetic solid frame with changing intensity to verify uniqueness
        intensity = (self.read_count * 17) % 256
        frame = np.full((self.frame_height, self.frame_width, 3), intensity, dtype=np.uint8)
        return True, frame

    def release(self) -> None:
        self._opened = False
        self.released = True


# Factory callback type for creating capture adapters
CaptureAdapterFactory = Callable[[str], VideoCaptureAdapter]


def _default_capture_factory(source_type: str) -> VideoCaptureAdapter:
    return OpenCVCaptureAdapter(source_type=source_type)


_default_factory: CaptureAdapterFactory = _default_capture_factory
_current_factory: CaptureAdapterFactory = _default_factory


def get_capture_adapter(source_type: str) -> VideoCaptureAdapter:
    """Obtain a capture adapter instance using the registered factory."""
    return _current_factory(source_type)


def set_capture_adapter_factory(factory: Optional[CaptureAdapterFactory]) -> None:
    """Override capture adapter factory (used in tests to inject fake capture adapters)."""
    global _current_factory
    _current_factory = factory if factory is not None else _default_factory


def reset_capture_adapter_factory() -> None:
    """Reset capture adapter factory to default production OpenCV adapter."""
    global _current_factory
    _current_factory = _default_factory
