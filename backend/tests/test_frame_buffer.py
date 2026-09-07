"""Unit tests for thread-safe bounded latest-frame buffer."""

from __future__ import annotations

from datetime import datetime, timezone
import threading
import time
import numpy as np

from backend.app.camera.frame_buffer import LatestFrameBuffer
from backend.app.camera.types import EncodedPreviewFrame, RawFrame


def test_latest_frame_buffer_bounded_depth():
    """Verify latest-frame buffer stores only 1 latest frame, dropping stale frames."""
    buffer = LatestFrameBuffer(camera_id=1)
    assert buffer.get_latest_raw() is None

    # Write frame 1
    f1 = RawFrame(
        frame_id=1,
        camera_id=1,
        captured_at=datetime.now(timezone.utc),
        monotonic_timestamp=time.monotonic(),
        width=100,
        height=100,
        data=np.zeros((100, 100, 3), dtype=np.uint8),
    )
    buffer.update_raw(f1)
    assert buffer.get_latest_raw().frame_id == 1
    assert buffer.total_replaced == 0

    # Write frame 2 without consuming frame 1
    f2 = RawFrame(
        frame_id=2,
        camera_id=1,
        captured_at=datetime.now(timezone.utc),
        monotonic_timestamp=time.monotonic(),
        width=100,
        height=100,
        data=np.ones((100, 100, 3), dtype=np.uint8),
    )
    buffer.update_raw(f2)
    assert buffer.get_latest_raw().frame_id == 2
    assert buffer.total_replaced == 1


def test_frame_buffer_defensive_copy():
    """Verify consumer copy prevents mutations to buffered data."""
    buffer = LatestFrameBuffer(camera_id=1)
    raw_arr = np.zeros((50, 50, 3), dtype=np.uint8)
    f = RawFrame(
        frame_id=10,
        camera_id=1,
        captured_at=datetime.now(timezone.utc),
        monotonic_timestamp=time.monotonic(),
        width=50,
        height=50,
        data=raw_arr,
    )
    buffer.update_raw(f)

    # Request defensive copy
    copied = buffer.get_latest_raw(copy=True)
    assert copied is not None
    copied.data[0, 0, 0] = 255  # Mutate copy

    # Original buffer remains intact
    buffered = buffer.get_latest_raw(copy=False)
    assert buffered.data[0, 0, 0] == 0


def test_preview_frame_storage_and_clear():
    """Verify preview frame storage and buffer clearance on stop."""
    buffer = LatestFrameBuffer(camera_id=42)
    p = EncodedPreviewFrame(
        frame_id=1,
        camera_id=42,
        encoded_at=datetime.now(timezone.utc),
        sequence=1,
        jpeg_bytes=b"fake_jpeg_bytes",
        width=320,
        height=240,
    )
    buffer.update_preview(p)
    assert buffer.get_latest_preview().jpeg_bytes == b"fake_jpeg_bytes"

    buffer.clear()
    assert buffer.get_latest_raw() is None
    assert buffer.get_latest_preview() is None


def test_frame_buffer_concurrent_access():
    """Verify thread safety under concurrent reader and writer load."""
    buffer = LatestFrameBuffer(camera_id=99)
    stop_event = threading.Event()

    def writer():
        for i in range(200):
            frame = RawFrame(
                frame_id=i,
                camera_id=99,
                captured_at=datetime.now(timezone.utc),
                monotonic_timestamp=time.monotonic(),
                width=32,
                height=32,
                data=np.full((32, 32, 3), i % 256, dtype=np.uint8),
            )
            buffer.update_raw(frame)
            time.sleep(0.001)
        stop_event.set()

    def reader():
        while not stop_event.is_set():
            _ = buffer.get_latest_raw(copy=True)
            time.sleep(0.002)

    threads = [
        threading.Thread(target=writer),
        threading.Thread(target=reader),
        threading.Thread(target=reader),
    ]

    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=5.0)

    assert buffer.get_latest_raw() is not None
