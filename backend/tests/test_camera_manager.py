"""Unit and lifecycle tests for CameraManager."""

from __future__ import annotations

import threading

from backend.app.camera.manager import CameraManager
from backend.app.camera.source import FakeCaptureAdapter
from backend.app.db.enums import CameraSourceType, CameraStatus
from backend.app.db.models.camera import Camera


def test_manager_start_and_duplicate_prevention():
    """Verify CameraManager starts camera and prevents duplicate worker creation."""
    manager = CameraManager()
    fake_adapter = FakeCaptureAdapter(can_open=True)
    manager.set_adapter_factory(lambda st: fake_adapter)

    cam = Camera(
        id=1,
        name="manager_cam_1",
        source_type=CameraSourceType.WEBCAM,
        device_index=0,
        status=CameraStatus.OFFLINE,
    )

    worker1 = manager.start_camera(cam)
    assert worker1.is_running()
    assert manager.get_worker(1) is worker1

    # Starting again returns the identical active worker instance
    worker2 = manager.start_camera(cam)
    assert worker2 is worker1

    manager.stop_camera(1)
    assert not worker1.is_running()
    assert manager.get_worker(1) is None


def test_manager_restart_camera():
    """Verify restart stops old worker and spawns a new worker with updated settings."""
    manager = CameraManager()
    manager.set_adapter_factory(lambda st: FakeCaptureAdapter(can_open=True))

    cam = Camera(
        id=2,
        name="manager_cam_2",
        source_type=CameraSourceType.WEBCAM,
        device_index=0,
        status=CameraStatus.OFFLINE,
    )

    worker1 = manager.start_camera(cam)
    assert worker1.is_running()

    # Restart
    worker2 = manager.restart_camera(cam)
    assert worker2 is not worker1
    assert not worker1.is_running()
    assert worker2.is_running()

    manager.stop_all()


def test_manager_test_connection_probe():
    """Verify test_connection probes without spawning a persistent worker."""
    manager = CameraManager()
    manager.set_adapter_factory(lambda st: FakeCaptureAdapter(can_open=True, frame_width=640, frame_height=480))

    result = manager.test_connection(source_type="WEBCAM", device_index=0)
    assert result.success is True
    assert result.frame_width == 640
    assert result.frame_height == 480
    assert result.elapsed_ms >= 0.0
    assert manager.get_worker(0) is None  # No persistent worker created


def test_manager_test_connection_probe_failure():
    """Verify test_connection returns failure result when adapter cannot open."""
    manager = CameraManager()
    manager.set_adapter_factory(lambda st: FakeCaptureAdapter(can_open=False))

    result = manager.test_connection(source_type="RTSP", rtsp_url="rtsp://10.0.0.1/stream")
    assert result.success is False
    assert result.safe_error_code == "OPEN_FAILED"


def test_manager_shutdown_proof():
    """Verify application shutdown stops all workers leaving zero active camera threads."""
    manager = CameraManager()
    manager.set_adapter_factory(lambda st: FakeCaptureAdapter(can_open=True))

    cams = [
        Camera(id=10, name="cam_10", source_type=CameraSourceType.WEBCAM, device_index=0),
        Camera(id=11, name="cam_11", source_type=CameraSourceType.WEBCAM, device_index=1),
        Camera(id=12, name="cam_12", source_type=CameraSourceType.WEBCAM, device_index=2),
    ]

    for c in cams:
        manager.start_camera(c)

    # Verify all 3 are running
    for c in cams:
        w = manager.get_worker(c.id)
        assert w is not None and w.is_running()

    # Trigger shutdown
    manager.stop_all(timeout=3.0)

    # Verify registry is cleared
    assert len(manager.get_all_telemetry()) == 0

    # Verify thread count: zero threads named 'presyn-camera-*' remain alive
    active_threads = threading.enumerate()
    camera_threads = [t for t in active_threads if t.name.startswith("presyn-camera-") and t.is_alive()]
    assert len(camera_threads) == 0, f"Leaked camera worker threads: {camera_threads}"
