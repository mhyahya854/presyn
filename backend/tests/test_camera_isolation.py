"""Integration test verifying multi-camera capture worker fault isolation."""

from __future__ import annotations

import time

from backend.app.camera.source import FakeCaptureAdapter
from backend.app.camera.worker import CameraCaptureWorker


def test_multi_camera_isolation():
    """Verify Camera A continues publishing frames while Camera B repeatedly fails without blocking."""
    # Camera A adapter succeeds indefinitely
    adapter_a = FakeCaptureAdapter(can_open=True, frame_width=320, frame_height=240)
    worker_a = CameraCaptureWorker(
        camera_id=101,
        camera_name="isolated_camera_a",
        source_type="WEBCAM",
        device_index=0,
        adapter_factory=lambda st: adapter_a,
        preview_fps=10,
    )

    # Camera B adapter fails immediately and repeatedly
    adapter_b = FakeCaptureAdapter(can_open=False)
    worker_b = CameraCaptureWorker(
        camera_id=102,
        camera_name="isolated_camera_b_failing",
        source_type="RTSP",
        rtsp_url="rtsp://192.168.99.99:554/dead",
        adapter_factory=lambda st: adapter_b,
        reconnect_initial_seconds=0.05,
        reconnect_max_seconds=0.2,
    )

    try:
        worker_a.start()
        worker_b.start()

        # Allow both workers to execute concurrently
        for _ in range(40):
            snap_a = worker_a.telemetry.get_snapshot()
            snap_b = worker_b.telemetry.get_snapshot()
            if snap_a.frames_decoded >= 5 and snap_b.reconnect_count >= 2:
                break
            time.sleep(0.05)

        snap_a = worker_a.telemetry.get_snapshot()
        snap_b = worker_b.telemetry.get_snapshot()

        # Camera A is completely healthy and unaffected by B
        assert snap_a.runtime_status == "ONLINE"
        assert snap_a.frames_decoded >= 5
        assert snap_a.read_failures == 0
        assert worker_a.is_running()

        # Camera B is safely isolated in its reconnect loop
        assert snap_b.runtime_status == "OFFLINE"
        assert snap_b.reconnect_count >= 2
        assert snap_b.frames_decoded == 0
        assert worker_b.is_running()

    finally:
        worker_a.stop(timeout=2.0)
        worker_b.stop(timeout=2.0)

        assert not worker_a.is_running()
        assert not worker_b.is_running()
