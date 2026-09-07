"""Integration test using a temporary synthetic video without faces or people."""

from __future__ import annotations

import os
import tempfile
import cv2
import numpy as np

from backend.app.camera.frame_buffer import LatestFrameBuffer
from backend.app.camera.types import RawFrame


def test_synthetic_video_lifecycle_and_decoding():
    """Verify OpenCV decoding, frame progression, latest-frame buffering, and cleanup with temporary synthetic video."""
    temp_dir = tempfile.mkdtemp(prefix="presyn_synthetic_")
    video_path = os.path.join(temp_dir, "test_synthetic_pattern.avi")

    width, height = 320, 240
    fps = 10
    total_frames = 15

    try:
        # Generate temporary synthetic video using geometric shapes and solid colors
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        writer = cv2.VideoWriter(video_path, fourcc, fps, (width, height))
        assert writer.isOpened(), "Could not create synthetic video writer"

        for i in range(total_frames):
            # Create synthetic frame: dark background with a moving white rectangle
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            rect_x = int((i * (width - 60)) / total_frames)
            cv2.rectangle(frame, (rect_x, 80), (rect_x + 50, 160), (255, 255, 255), -1)
            cv2.circle(frame, (160, 40), 20, (0, 128, 255), -1)
            writer.write(frame)

        writer.release()
        assert os.path.exists(video_path)
        assert os.path.getsize(video_path) > 0

        # Decode using OpenCV VideoCapture
        cap = cv2.VideoCapture(video_path)
        assert cap.isOpened()

        buffer = LatestFrameBuffer(camera_id=999)
        decoded_count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret or frame is None:
                break
            decoded_count += 1
            assert frame.shape == (height, width, 3)

            raw_frame = RawFrame(
                frame_id=decoded_count,
                camera_id=999,
                captured_at=None,  # type: ignore[arg-type]
                monotonic_timestamp=float(decoded_count),
                width=width,
                height=height,
                data=frame,
            )
            buffer.update_raw(raw_frame)

            # Test JPEG encoding
            encode_ret, jpeg_buf = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 75])
            assert encode_ret is True
            assert len(jpeg_buf) > 0

        cap.release()

        assert decoded_count == total_frames
        assert buffer.get_latest_raw().frame_id == total_frames
        assert buffer.total_replaced == total_frames - 1

    finally:
        # Strictly delete temporary synthetic video file and directory
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)

    assert not os.path.exists(video_path), "Synthetic video was not cleaned up"
