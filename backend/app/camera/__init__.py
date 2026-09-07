"""Camera Subsystem for Presyn Platform.

Provides decoupled CPU-based video capture, resilient reconnects, latest-frame buffering,
real-time telemetry, and binary preview frame streaming.
"""

from backend.app.camera.credentials import (
    CredentialsUnavailableError,
    resolve_camera_runtime_source,
    validate_credential_ref,
)
from backend.app.camera.events import LiveEventHub, live_event_hub
from backend.app.camera.frame_buffer import LatestFrameBuffer
from backend.app.camera.manager import CameraManager, camera_manager
from backend.app.camera.source import (
    CaptureAdapterFactory,
    FakeCaptureAdapter,
    OpenCVCaptureAdapter,
    VideoCaptureAdapter,
    get_capture_adapter,
    reset_capture_adapter_factory,
    set_capture_adapter_factory,
)
from backend.app.camera.telemetry import CameraTelemetryCollector
from backend.app.camera.types import (
    CameraTelemetryState,
    CameraTestResult,
    EncodedPreviewFrame,
    RawFrame,
)
from backend.app.camera.worker import CameraCaptureWorker

__all__ = [
    "CameraCaptureWorker",
    "CameraManager",
    "CameraTelemetryCollector",
    "CameraTelemetryState",
    "CameraTestResult",
    "CaptureAdapterFactory",
    "CredentialsUnavailableError",
    "EncodedPreviewFrame",
    "FakeCaptureAdapter",
    "LatestFrameBuffer",
    "LiveEventHub",
    "OpenCVCaptureAdapter",
    "RawFrame",
    "VideoCaptureAdapter",
    "camera_manager",
    "get_capture_adapter",
    "live_event_hub",
    "reset_capture_adapter_factory",
    "resolve_camera_runtime_source",
    "set_capture_adapter_factory",
    "validate_credential_ref",
]
