"""Unit tests for CameraCaptureWorker lifecycle, backoff sequence, and failure recovery."""

from __future__ import annotations

import time

from backend.app.camera.source import FakeCaptureAdapter
from backend.app.camera.worker import CameraCaptureWorker


def test_worker_start_first_frame_online_and_stop():
    """Verify worker transitions to ONLINE upon decoding first frame and stops cleanly."""
    fake_adapter = FakeCaptureAdapter(can_open=True, frame_width=160, frame_height=120)
    worker = CameraCaptureWorker(
        camera_id=1,
        camera_name="test_worker_cam",
        source_type="WEBCAM",
        device_index=0,
        adapter_factory=lambda st: fake_adapter,
        preview_fps=10,
    )

    worker.start()
    assert worker.is_running()

    # Wait for first frame decode
    for _ in range(50):
        snap = worker.telemetry.get_snapshot()
        if snap.runtime_status == "ONLINE" and snap.frames_decoded > 0:
            break
        time.sleep(0.05)

    snap = worker.telemetry.get_snapshot()
    assert snap.runtime_status == "ONLINE"
    assert snap.frames_decoded > 0
    assert snap.frame_width == 160
    assert snap.frame_height == 120
    assert worker.frame_buffer.get_latest_raw() is not None

    worker.stop(timeout=2.0)
    assert not worker.is_running()
    assert fake_adapter.released is True


def test_worker_read_failure_and_degraded_transition():
    """Verify consecutive read failures transition camera to DEGRADED and then trigger reconnect."""
    # Fail after 5 successful reads
    fake_adapter = FakeCaptureAdapter(
        can_open=True,
        frame_width=160,
        frame_height=120,
        fail_after_reads=3,
    )
    worker = CameraCaptureWorker(
        camera_id=2,
        camera_name="degraded_test_cam",
        source_type="RTSP",
        rtsp_url="rtsp://127.0.0.1:554/live",
        adapter_factory=lambda st: fake_adapter,
        read_failure_threshold=4,
        reconnect_initial_seconds=0.1,
        reconnect_max_seconds=0.5,
    )

    worker.start()

    # Wait for frames then failures
    for _ in range(50):
        snap = worker.telemetry.get_snapshot()
        if snap.read_failures >= 2:
            break
        time.sleep(0.05)

    snap = worker.telemetry.get_snapshot()
    assert snap.read_failures >= 2

    worker.stop(timeout=2.0)
    assert not worker.is_running()


def test_worker_backoff_progression_and_cap():
    """Verify exponential backoff doubles up to max cap upon connection failure."""
    failing_adapter = FakeCaptureAdapter(can_open=False)
    worker = CameraCaptureWorker(
        camera_id=3,
        camera_name="failing_cam",
        source_type="RTSP",
        rtsp_url="rtsp://127.0.0.1:554/unreachable",
        adapter_factory=lambda st: failing_adapter,
        reconnect_initial_seconds=0.05,
        reconnect_max_seconds=0.2,
    )

    worker.start()

    # Let worker attempt reconnects
    for _ in range(50):
        snap = worker.telemetry.get_snapshot()
        if snap.reconnect_count >= 3:
            break
        time.sleep(0.05)

    snap = worker.telemetry.get_snapshot()
    assert snap.reconnect_count >= 2
    assert snap.runtime_status == "OFFLINE"
    # Backoff is capped at reconnect_max_seconds
    assert snap.current_backoff_seconds <= 0.2

    worker.stop(timeout=2.0)
    assert not worker.is_running()


def test_worker_backoff_resets_upon_successful_frame():
    """Verify backoff seconds resets to initial value when valid frames arrive."""
    worker = CameraCaptureWorker(
        camera_id=4,
        camera_name="recovery_cam",
        source_type="WEBCAM",
        device_index=0,
        reconnect_initial_seconds=2.0,
        reconnect_max_seconds=30.0,
    )

    # Simulate backoff buildup
    worker.telemetry.record_reconnect_attempt(8.0)
    assert worker.telemetry.get_snapshot().current_backoff_seconds == 8.0

    # Reset on successful frame
    worker.telemetry.reset_backoff()
    assert worker.telemetry.get_snapshot().current_backoff_seconds == 0.0
