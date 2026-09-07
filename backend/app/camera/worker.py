"""Independent capture worker thread for an individual camera stream."""

from __future__ import annotations

from datetime import datetime, timezone
import threading
import time
from typing import Optional
import cv2

from backend.app.camera.credentials import (
    CredentialsUnavailableError,
    resolve_camera_runtime_source,
)
from backend.app.camera.events import live_event_hub
from backend.app.camera.frame_buffer import LatestFrameBuffer
from backend.app.camera.source import (
    CaptureAdapterFactory,
    VideoCaptureAdapter,
    get_capture_adapter,
)
from backend.app.camera.telemetry import CameraTelemetryCollector
from backend.app.camera.types import EncodedPreviewFrame, RawFrame
from backend.app.core.exceptions import ValidationException
from backend.app.core.logging import logger


class CameraCaptureWorker:
    """Dedicated background capture worker running one thread per camera."""

    def __init__(
        self,
        camera_id: int,
        camera_name: str,
        source_type: str,
        device_index: Optional[int] = None,
        rtsp_url: Optional[str] = None,
        credential_ref: Optional[str] = None,
        target_fps: int = 5,
        reconnect_initial_seconds: float = 2.0,
        reconnect_max_seconds: float = 30.0,
        read_failure_threshold: int = 5,
        preview_fps: int = 10,
        jpeg_quality: int = 75,
        preview_max_width: int = 640,
        adapter_factory: Optional[CaptureAdapterFactory] = None,
    ) -> None:
        self.camera_id = camera_id
        self.camera_name = camera_name
        self.source_type = source_type.upper()
        self.device_index = device_index
        self.rtsp_url = rtsp_url
        self.credential_ref = credential_ref

        self.target_fps = target_fps
        self.reconnect_initial_seconds = reconnect_initial_seconds
        self.reconnect_max_seconds = reconnect_max_seconds
        self.read_failure_threshold = read_failure_threshold
        self.preview_fps = preview_fps
        self.jpeg_quality = jpeg_quality
        self.preview_max_width = preview_max_width

        self.frame_buffer = LatestFrameBuffer(camera_id=camera_id)
        self.telemetry = CameraTelemetryCollector(
            camera_id=camera_id,
            camera_name=camera_name,
            source_type=self.source_type,
        )

        self._adapter_factory = adapter_factory
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._disabled = False

    def is_running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def start(self) -> None:
        """Start the background capture worker thread."""
        if self.is_running():
            return

        self._stop_event.clear()
        self._disabled = False
        self.telemetry.set_worker_running(True)
        self._thread = threading.Thread(
            target=self._run_capture_loop,
            name=f"presyn-camera-{self.camera_id}",
            daemon=True,
        )
        self._thread.start()
        logger.info("Started camera worker thread for camera_id=%d name=%s", self.camera_id, self.camera_name)

    def stop(self, timeout: float = 3.0, mark_disabled: bool = True) -> None:
        """Signal the capture loop to stop, release handles, and join thread."""
        self._disabled = mark_disabled
        self._stop_event.set()

        if self._thread is not None and self._thread.is_alive():
            self._thread.join(timeout=timeout)
            if self._thread.is_alive():
                logger.warning("Camera worker thread for camera_id=%d did not exit cleanly within timeout", self.camera_id)

        self._thread = None
        self.frame_buffer.clear()
        self.telemetry.set_worker_running(False)
        self.telemetry.set_status("DISABLED" if mark_disabled else "OFFLINE")

    def _publish_event(self, event_type: str) -> None:
        snapshot = self.telemetry.get_snapshot()
        payload = {
            "runtime_status": snapshot.runtime_status,
            "capture_fps": snapshot.capture_fps,
            "preview_fps": snapshot.preview_fps,
            "inference_fps": None,
            "frames_decoded": snapshot.frames_decoded,
            "last_frame_age_ms": snapshot.last_frame_age_ms,
            "safe_error_code": snapshot.safe_error_code,
        }
        live_event_hub.publish_from_thread(
            event_type=event_type,
            camera_id=self.camera_id,
            camera_name=self.camera_name,
            payload=payload,
        )

    def _run_capture_loop(self) -> None:
        """Continuous, resilient capture loop with exponential backoff and error recovery."""
        backoff_seconds = self.reconnect_initial_seconds

        while not self._stop_event.is_set():
            # 1. Resolve runtime source in memory (strictly never logging secrets)
            try:
                resolved_source = resolve_camera_runtime_source(
                    source_type=self.source_type,
                    device_index=self.device_index,
                    rtsp_url=self.rtsp_url,
                    credential_ref=self.credential_ref,
                )
            except (CredentialsUnavailableError, ValidationException) as exc:
                self.telemetry.set_status("ERROR")
                self.telemetry.record_read_failure(exc.error_code)
                self._publish_event("CAMERA_ERROR")
                logger.warning(
                    "Camera credential resolution error for camera_id=%d code=%s",
                    self.camera_id,
                    exc.error_code,
                )
                self._stop_event.wait(backoff_seconds)
                backoff_seconds = min(backoff_seconds * 2, self.reconnect_max_seconds)
                continue
            except Exception:
                self.telemetry.set_status("ERROR")
                self.telemetry.record_read_failure("SOURCE_RESOLUTION_FAILED")
                self._publish_event("CAMERA_ERROR")
                self._stop_event.wait(backoff_seconds)
                backoff_seconds = min(backoff_seconds * 2, self.reconnect_max_seconds)
                continue

            # 2. Attempt capture connection
            self.telemetry.set_status("CONNECTING")
            self._publish_event("CAMERA_CONNECTING")

            adapter: VideoCaptureAdapter = (
                self._adapter_factory(self.source_type)
                if self._adapter_factory
                else get_capture_adapter(self.source_type)
            )

            opened = False
            try:
                opened = adapter.open(resolved_source)
            except Exception:
                opened = False

            if not opened or not adapter.is_opened():
                self.telemetry.set_status("OFFLINE")
                self.telemetry.record_read_failure("CONNECTION_FAILED")
                self.telemetry.record_reconnect_attempt(backoff_seconds)
                self._publish_event("CAMERA_OFFLINE")
                adapter.release()
                self._stop_event.wait(backoff_seconds)
                backoff_seconds = min(backoff_seconds * 2, self.reconnect_max_seconds)
                continue

            # 3. Connection opened successfully: enter frame reading loop
            self.telemetry.record_successful_open()
            consecutive_read_failures = 0
            has_decoded_first_frame = False
            preview_interval = 1.0 / max(1, self.preview_fps)
            last_preview_time = 0.0
            raw_frame_id = 0
            preview_sequence = 0

            try:
                while not self._stop_event.is_set() and adapter.is_opened():
                    success, frame = adapter.read()

                    if not success or frame is None:
                        consecutive_read_failures += 1
                        self.telemetry.record_read_failure("READ_FRAME_FAILED")

                        if consecutive_read_failures >= self.read_failure_threshold:
                            logger.warning(
                                "Camera camera_id=%d exceeded read failure threshold (%d)",
                                self.camera_id,
                                self.read_failure_threshold,
                            )
                            break
                        elif consecutive_read_failures >= 2:
                            self.telemetry.set_status("DEGRADED")
                            self._publish_event("CAMERA_DEGRADED")

                        # Brief sleep to avoid busy-looping during intermittent read drops
                        self._stop_event.wait(0.01)
                        continue

                    # Successful frame decoded
                    consecutive_read_failures = 0
                    height, width = frame.shape[:2]

                    if not has_decoded_first_frame:
                        has_decoded_first_frame = True
                        self.telemetry.set_status("ONLINE")
                        self.telemetry.reset_backoff()
                        backoff_seconds = self.reconnect_initial_seconds
                        self._publish_event("CAMERA_ONLINE")

                    now_utc = datetime.now(timezone.utc)
                    now_mono = time.monotonic()
                    raw_frame_id += 1

                    raw_frame = RawFrame(
                        frame_id=raw_frame_id,
                        camera_id=self.camera_id,
                        captured_at=now_utc,
                        monotonic_timestamp=now_mono,
                        width=width,
                        height=height,
                        data=frame,
                    )
                    self.frame_buffer.update_raw(raw_frame)
                    self.telemetry.record_frame_decoded(width, height)

                    # Encode throttled JPEG preview
                    if (now_mono - last_preview_time) >= preview_interval:
                        last_preview_time = now_mono
                        preview_sequence += 1

                        if width > self.preview_max_width:
                            scale = self.preview_max_width / float(width)
                            target_h = int(height * scale)
                            preview_img = cv2.resize(frame, (self.preview_max_width, target_h), interpolation=cv2.INTER_AREA)
                        else:
                            preview_img = frame

                        encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), self.jpeg_quality]
                        encode_success, jpeg_buf = cv2.imencode(".jpg", preview_img, encode_params)

                        if encode_success and jpeg_buf is not None:
                            preview_frame = EncodedPreviewFrame(
                                frame_id=raw_frame_id,
                                camera_id=self.camera_id,
                                encoded_at=now_utc,
                                sequence=preview_sequence,
                                jpeg_bytes=jpeg_buf.tobytes(),
                                width=preview_img.shape[1],
                                height=preview_img.shape[0],
                            )
                            self.frame_buffer.update_preview(preview_frame)
                            self.telemetry.record_preview_published()

            finally:
                adapter.release()

            # If loop broke due to read failure and worker is not stopping, prepare reconnect
            if not self._stop_event.is_set():
                self.telemetry.set_status("OFFLINE")
                self.telemetry.record_reconnect_attempt(backoff_seconds)
                self._publish_event("CAMERA_OFFLINE")
                self._stop_event.wait(backoff_seconds)
                backoff_seconds = min(backoff_seconds * 2, self.reconnect_max_seconds)

        # Worker shutdown
        self.frame_buffer.clear()
        self.telemetry.set_worker_running(False)
        final_status = "DISABLED" if self._disabled else "OFFLINE"
        self.telemetry.set_status(final_status)
        self._publish_event(f"CAMERA_{final_status}")
