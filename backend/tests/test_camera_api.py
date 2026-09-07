"""Integration tests for Camera REST API endpoints."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from backend.app.camera.manager import camera_manager
from backend.app.camera.source import FakeCaptureAdapter


@pytest.fixture(autouse=True)
def setup_fake_camera_manager():
    """Ensure tests run with fake capture adapter and clean up workers afterwards."""
    fake_adapter = FakeCaptureAdapter(can_open=True, frame_width=640, frame_height=480)
    camera_manager.set_adapter_factory(lambda st: fake_adapter)
    yield
    camera_manager.stop_all(timeout=1.0)
    camera_manager.set_adapter_factory(None)


def test_camera_crud_lifecycle(client: TestClient):
    """Verify complete CRUD lifecycle for camera resources."""
    # 1. List initially empty
    res = client.get("/api/v1/cameras")
    assert res.status_code == 200
    assert res.json() == []

    # 2. Create WEBCAM
    webcam_payload = {
        "name": "Reception Desk Webcam",
        "location": "Front Reception",
        "source_type": "WEBCAM",
        "device_index": 0,
        "target_fps": 10,
        "reconnect_delay": 3,
    }
    create_res = client.post("/api/v1/cameras", json=webcam_payload)
    assert create_res.status_code == 201
    created_webcam = create_res.json()
    cam_id = created_webcam["id"]
    assert created_webcam["name"] == "Reception Desk Webcam"
    assert created_webcam["source_type"] == "WEBCAM"
    assert created_webcam["device_index"] == 0
    assert created_webcam["rtsp_url"] is None
    assert created_webcam["is_active"] is True

    # 3. Get by ID
    get_res = client.get(f"/api/v1/cameras/{cam_id}")
    assert get_res.status_code == 200
    assert get_res.json()["name"] == "Reception Desk Webcam"

    # 4. Patch camera
    patch_res = client.patch(f"/api/v1/cameras/{cam_id}", json={"location": "Main Entrance Lobby"})
    assert patch_res.status_code == 200
    assert patch_res.json()["location"] == "Main Entrance Lobby"

    # 5. Delete camera
    del_res = client.delete(f"/api/v1/cameras/{cam_id}")
    assert del_res.status_code == 204

    # 6. Verify 404 after deletion
    assert client.get(f"/api/v1/cameras/{cam_id}").status_code == 404


def test_create_rtsp_camera_with_credential_ref(client: TestClient):
    """Verify RTSP camera creation with credential_ref and credential-free URL."""
    payload = {
        "name": "Perimeter East Camera",
        "location": "East Boundary Gate",
        "source_type": "RTSP",
        "rtsp_url": "rtsp://192.168.1.120:554/live/ch0",
        "credential_ref": "EAST_GATE_CAM",
        "target_fps": 5,
        "reconnect_delay": 5,
    }
    res = client.post("/api/v1/cameras", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data["credential_ref"] == "EAST_GATE_CAM"
    assert data["rtsp_url"] == "rtsp://192.168.1.120:554/live/ch0"
    assert data["device_index"] is None


def test_reject_inline_credentials_in_create_endpoint(client: TestClient):
    """Verify API rejects inline username/password in RTSP URL without echoing secrets."""
    payload = {
        "name": "Insecure Camera",
        "source_type": "RTSP",
        "rtsp_url": "rtsp://admin:super_secret_pass@192.168.1.50:554/feed",
    }
    res = client.post("/api/v1/cameras", json=payload)
    assert res.status_code == 422
    err_text = res.text
    assert "super_secret_pass" not in err_text
    assert "admin" not in err_text


def test_reject_sensitive_query_parameters_in_create_endpoint(client: TestClient):
    """Verify API rejects sensitive query parameters in RTSP URL without echoing secrets."""
    payload = {
        "name": "Token Leak Camera",
        "source_type": "RTSP",
        "rtsp_url": "rtsp://192.168.1.50:554/feed?token=sensitive_token_value",
    }
    res = client.post("/api/v1/cameras", json=payload)
    assert res.status_code == 422
    err_text = res.text
    assert "sensitive_token_value" not in err_text
    assert "RTSP URL contains a sensitive query parameter" in err_text


def test_reject_invalid_source_type_combinations(client: TestClient):
    """Verify API validates WEBCAM vs RTSP mutual exclusivity."""
    # WEBCAM missing device_index
    res1 = client.post("/api/v1/cameras", json={"name": "Bad Webcam", "source_type": "WEBCAM"})
    assert res1.status_code == 422

    # WEBCAM with rtsp_url
    res2 = client.post(
        "/api/v1/cameras",
        json={"name": "Bad Webcam 2", "source_type": "WEBCAM", "device_index": 0, "rtsp_url": "rtsp://test/live"},
    )
    assert res2.status_code == 422

    # RTSP with device_index
    res3 = client.post(
        "/api/v1/cameras",
        json={"name": "Bad RTSP", "source_type": "RTSP", "device_index": 0, "rtsp_url": "rtsp://test/live"},
    )
    assert res3.status_code == 422


def test_camera_start_stop_endpoints(client: TestClient):
    """Verify explicit start and stop operational endpoints."""
    # Create camera
    create_res = client.post(
        "/api/v1/cameras",
        json={"name": "StartStop Cam", "source_type": "WEBCAM", "device_index": 1},
    )
    cam_id = create_res.json()["id"]

    # Stop camera
    stop_res = client.post(f"/api/v1/cameras/{cam_id}/stop")
    assert stop_res.status_code == 200
    assert stop_res.json()["is_active"] is False
    assert stop_res.json()["status"] == "DISABLED"

    # Start camera
    start_res = client.post(f"/api/v1/cameras/{cam_id}/start")
    assert start_res.status_code == 200
    assert start_res.json()["is_active"] is True


def test_camera_test_connection_endpoint(client: TestClient):
    """Verify connection probe endpoint returns structured test result."""
    create_res = client.post(
        "/api/v1/cameras",
        json={"name": "Probe Cam", "source_type": "WEBCAM", "device_index": 0},
    )
    cam_id = create_res.json()["id"]

    test_res = client.post(f"/api/v1/cameras/{cam_id}/test")
    assert test_res.status_code == 200
    data = test_res.json()
    assert data["success"] is True
    assert data["camera_id"] == cam_id
    assert data["frame_width"] == 640
    assert data["frame_height"] == 480
    assert data["elapsed_ms"] >= 0.0


def test_camera_telemetry_endpoint(client: TestClient):
    """Verify telemetry endpoint returns real metrics without fake values."""
    create_res = client.post(
        "/api/v1/cameras",
        json={"name": "Telemetry Cam", "source_type": "WEBCAM", "device_index": 0},
    )
    cam_id = create_res.json()["id"]

    telem_res = client.get(f"/api/v1/cameras/{cam_id}/telemetry")
    assert telem_res.status_code == 200
    data = telem_res.json()
    assert data["camera_id"] == cam_id
    assert data["inference_fps"] is None  # Truthfully None in Phase 02
    assert "capture_fps" in data
    assert "preview_fps" in data
    assert "frames_decoded" in data
