"""Integration tests for WebSocket live events and binary preview frames."""

from __future__ import annotations

import cv2
import numpy as np
import pytest
from fastapi.testclient import TestClient

from backend.app.camera.events import live_event_hub
from backend.app.camera.manager import camera_manager
from backend.app.camera.source import FakeCaptureAdapter
from backend.app.db.enums import CameraSourceType
from backend.app.db.models.camera import Camera


@pytest.fixture(autouse=True)
def clean_manager_and_hub():
    yield
    camera_manager.stop_all(timeout=1.0)
    live_event_hub.shutdown()


def test_ws_live_events_connection_and_broadcast(client: TestClient):
    """Verify /api/v1/ws/live connects, receives handshake, and receives truthful camera events."""
    with client.websocket_connect("/api/v1/ws/live") as ws:
        # Handshake
        handshake = ws.receive_json()
        assert handshake["event_type"] == "CONNECTION_ESTABLISHED"

        # Broadcast a simulated camera event through hub
        live_event_hub.publish_from_thread(
            event_type="CAMERA_ONLINE",
            camera_id=7,
            camera_name="Main Gate",
            payload={"runtime_status": "ONLINE", "capture_fps": 15.0},
        )

        event = ws.receive_json()
        assert event["event_type"] == "CAMERA_ONLINE"
        assert event["camera_id"] == 7
        assert event["camera_name"] == "Main Gate"
        assert event["payload"]["runtime_status"] == "ONLINE"
        assert event["payload"]["capture_fps"] == 15.0

        # Truthful schema: no fabricated recognition or person tracking fields
        assert event["face"] is None
        assert event["identity"] is None
        assert event["spatial"] is None
        assert event["activity"] is None


def test_ws_camera_frames_binary_stream(client: TestClient, db_session):
    """Verify /api/v1/ws/cameras/{id}/frames streams binary JPEG bytes that decode into valid image."""
    # Create and start a camera with fake capture adapter
    fake_adapter = FakeCaptureAdapter(can_open=True, frame_width=320, frame_height=240)
    camera_manager.set_adapter_factory(lambda st: fake_adapter)

    cam = Camera(
        id=77,
        name="stream_test_cam",
        source_type=CameraSourceType.WEBCAM,
        device_index=0,
        is_active=True,
    )
    db_session.add(cam)
    db_session.flush()

    camera_manager.start_camera(cam)

    with client.websocket_connect(f"/api/v1/ws/cameras/{cam.id}/frames") as ws:
        # Stream info greeting
        info = ws.receive_json()
        assert info["type"] == "STREAM_INFO"
        assert info["camera_id"] == cam.id

        # Receive binary JPEG frame
        frame_bytes = ws.receive_bytes()
        assert isinstance(frame_bytes, bytes)
        assert len(frame_bytes) > 0

        # Decode JPEG bytes using OpenCV to verify image validity
        np_arr = np.frombuffer(frame_bytes, dtype=np.uint8)
        decoded_img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        assert decoded_img is not None
        assert decoded_img.shape[0] > 0
        assert decoded_img.shape[1] > 0

    camera_manager.stop_camera(cam.id)


def test_ws_offline_camera_stream_info(client: TestClient):
    """Verify WebSocket connection to offline camera returns truthful stream-info message."""
    with client.websocket_connect("/api/v1/ws/cameras/9999/frames") as ws:
        info = ws.receive_json()
        assert info["type"] == "STREAM_INFO"
        assert info["status"] == "OFFLINE"
        assert "offline or not running" in info["message"]
