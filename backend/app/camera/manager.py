"""Multi-camera runtime lifecycle manager and worker registry."""

from __future__ import annotations

import threading
import time
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from backend.app.camera.credentials import resolve_camera_runtime_source
from backend.app.camera.events import live_event_hub
from backend.app.camera.source import (
    CaptureAdapterFactory,
    VideoCaptureAdapter,
    get_capture_adapter,
)
from backend.app.camera.types import CameraTelemetryState, CameraTestResult
from backend.app.camera.worker import CameraCaptureWorker
from backend.app.core.config import settings
from backend.app.core.logging import logger
from backend.app.db.models.camera import Camera


class CameraManager:
    """Singleton runtime manager controlling capture workers and probe requests."""

    def __init__(self) -> None:
        self._workers: Dict[int, CameraCaptureWorker] = {}
        self._lock = threading.Lock()
        self._adapter_factory: Optional[CaptureAdapterFactory] = None

    def set_adapter_factory(self, factory: Optional[CaptureAdapterFactory]) -> None:
        """Inject adapter factory (used in automated tests)."""
        self._adapter_factory = factory

    def get_worker(self, camera_id: int) -> Optional[CameraCaptureWorker]:
        """Look up active capture worker by camera ID."""
        with self._lock:
            return self._workers.get(camera_id)

    def start_camera(self, camera: Camera) -> CameraCaptureWorker:
        """Start a dedicated capture worker for the given camera, preventing duplicates."""
        with self._lock:
            existing = self._workers.get(camera.id)
            if existing is not None:
                if existing.is_running():
                    return existing
                # Clean up inactive previous worker instance
                self._workers.pop(camera.id, None)

            source_val = (
                camera.source_type.value
                if hasattr(camera.source_type, "value")
                else str(camera.source_type)
            )

            # Camera-specific reconnect delay or platform global defaults
            initial_backoff = float(
                camera.reconnect_delay
                if (camera.reconnect_delay is not None and camera.reconnect_delay > 0)
                else settings.CAMERA_RECONNECT_INITIAL_SECONDS
            )

            worker = CameraCaptureWorker(
                camera_id=camera.id,
                camera_name=camera.name,
                source_type=source_val,
                device_index=camera.device_index,
                rtsp_url=camera.rtsp_url,
                credential_ref=camera.credential_ref,
                target_fps=camera.target_fps or settings.PROCESSING_FPS,
                reconnect_initial_seconds=initial_backoff,
                reconnect_max_seconds=float(settings.CAMERA_RECONNECT_MAX_SECONDS),
                read_failure_threshold=settings.CAMERA_READ_FAILURE_THRESHOLD,
                preview_fps=settings.CAMERA_PREVIEW_FPS,
                jpeg_quality=settings.CAMERA_JPEG_QUALITY,
                preview_max_width=settings.CAMERA_PREVIEW_MAX_WIDTH,
                adapter_factory=self._adapter_factory,
            )
            self._workers[camera.id] = worker

        # Launch background thread outside the registry lock
        worker.start()
        return worker

    def stop_camera(self, camera_id: int, timeout: float = 3.0) -> Optional[CameraCaptureWorker]:
        """Stop and unregister the capture worker for the specified camera."""
        with self._lock:
            worker = self._workers.pop(camera_id, None)

        if worker is not None:
            worker.stop(timeout=timeout, mark_disabled=True)
            return worker
        return None

    def restart_camera(self, camera: Camera, timeout: float = 3.0) -> CameraCaptureWorker:
        """Safely stop an existing worker and start a fresh worker with updated configuration."""
        self.stop_camera(camera.id, timeout=timeout)
        return self.start_camera(camera)

    def get_telemetry(self, camera_id: int) -> Optional[CameraTelemetryState]:
        """Fetch real point-in-time telemetry snapshot for a specific camera."""
        worker = self.get_worker(camera_id)
        if worker is not None:
            return worker.telemetry.get_snapshot()
        return None

    def get_all_telemetry(self) -> List[CameraTelemetryState]:
        """Fetch telemetry snapshots for all registered camera workers."""
        with self._lock:
            workers = list(self._workers.values())
        return [w.telemetry.get_snapshot() for w in workers]

    def test_connection(
        self,
        source_type: str,
        device_index: Optional[int] = None,
        rtsp_url: Optional[str] = None,
        credential_ref: Optional[str] = None,
        camera_id: Optional[int] = None,
        timeout_ms: int = 5000,
    ) -> CameraTestResult:
        """Perform a safe, short-lived capture probe without storing credentials or frames."""
        t0 = time.perf_counter()

        try:
            resolved_source = resolve_camera_runtime_source(
                source_type=source_type,
                device_index=device_index,
                rtsp_url=rtsp_url,
                credential_ref=credential_ref,
            )
        except Exception as exc:
            elapsed_ms = round((time.perf_counter() - t0) * 1000, 1)
            safe_code = getattr(exc, "error_code", "CREDENTIAL_RESOLUTION_FAILED")
            return CameraTestResult(
                success=False,
                camera_id=camera_id,
                source_type=source_type,
                elapsed_ms=elapsed_ms,
                safe_error_code=safe_code,
                message="Failed to resolve camera authentication credentials.",
            )

        adapter: VideoCaptureAdapter = (
            self._adapter_factory(source_type)
            if self._adapter_factory
            else get_capture_adapter(source_type)
        )

        try:
            opened = adapter.open(resolved_source)
            if not opened or not adapter.is_opened():
                elapsed_ms = round((time.perf_counter() - t0) * 1000, 1)
                return CameraTestResult(
                    success=False,
                    camera_id=camera_id,
                    source_type=source_type,
                    elapsed_ms=elapsed_ms,
                    safe_error_code="OPEN_FAILED",
                    message="Failed to open camera capture stream.",
                )

            success, frame = adapter.read()
            elapsed_ms = round((time.perf_counter() - t0) * 1000, 1)

            if not success or frame is None:
                return CameraTestResult(
                    success=False,
                    camera_id=camera_id,
                    source_type=source_type,
                    elapsed_ms=elapsed_ms,
                    safe_error_code="READ_FAILED",
                    message="Camera connection established, but frame decoding failed.",
                )

            h, w = frame.shape[:2]
            return CameraTestResult(
                success=True,
                camera_id=camera_id,
                source_type=source_type,
                elapsed_ms=elapsed_ms,
                frame_width=w,
                frame_height=h,
                message="Camera probe succeeded and decoded valid frame.",
            )

        except Exception:
            elapsed_ms = round((time.perf_counter() - t0) * 1000, 1)
            return CameraTestResult(
                success=False,
                camera_id=camera_id,
                source_type=source_type,
                elapsed_ms=elapsed_ms,
                safe_error_code="PROBE_EXCEPTION",
                message="Encountered unexpected error during camera probe.",
            )
        finally:
            adapter.release()

    def startup_active_cameras(self, db: Session) -> int:
        """Start all cameras marked is_active=True in the database during application startup."""
        try:
            active_cameras = db.query(Camera).filter(Camera.is_active.is_(True)).all()
            started_count = 0
            for cam in active_cameras:
                try:
                    self.start_camera(cam)
                    started_count += 1
                except Exception as exc:
                    logger.error("Failed to start camera_id=%d during startup: %s", cam.id, exc)
            logger.info("Startup completed: launched %d active camera workers", started_count)
            return started_count
        except Exception as exc:
            logger.warning("Could not query cameras during startup (e.g. fresh DB before migration): %s", exc)
            return 0

    def get_subsystem_summary(self, total_configured: int = 0) -> Dict[str, Any]:
        """Generate aggregate camera subsystem metrics for health endpoints without leaking URLs."""
        with self._lock:
            workers = list(self._workers.values())

        running = 0
        online = 0
        degraded = 0
        offline = 0

        for w in workers:
            if w.is_running():
                running += 1
            status = w.telemetry.get_snapshot().runtime_status
            if status == "ONLINE":
                online += 1
            elif status == "DEGRADED":
                degraded += 1
            else:
                offline += 1

        overall = "healthy" if online > 0 or running == 0 else "degraded"
        if running > 0 and online == 0:
            overall = "offline" if degraded == 0 else "degraded"

        return {
            "status": overall,
            "configured": total_configured,
            "running": running,
            "online": online,
            "degraded": degraded,
            "offline": offline,
        }

    def stop_all(self, timeout: float = 3.0) -> None:
        """Stop all running camera worker threads cleanly on application shutdown."""
        with self._lock:
            workers = list(self._workers.values())
            self._workers.clear()

        logger.info("Stopping %d camera worker threads...", len(workers))
        for worker in workers:
            worker.stop(timeout=timeout, mark_disabled=False)

        live_event_hub.shutdown()
        logger.info("All camera workers stopped.")


# Global singleton instance
camera_manager = CameraManager()
