"""Unit tests for runtime camera credential resolution and secret boundaries."""

from __future__ import annotations

import pytest

from backend.app.camera.credentials import (
    CredentialsUnavailableError,
    resolve_camera_runtime_source,
    validate_credential_ref,
)
from backend.app.core.exceptions import ValidationException
from backend.app.db.models.camera import Camera


def test_credential_ref_validation():
    """Verify strict uppercase alphanumeric format validation for credential references."""
    assert validate_credential_ref(None) is None
    assert validate_credential_ref("") is None
    assert validate_credential_ref("MAIN_ENTRANCE") == "MAIN_ENTRANCE"
    assert validate_credential_ref("CAM_101_FLOOR2") == "CAM_101_FLOOR2"

    with pytest.raises(ValidationException):
        validate_credential_ref("invalid-hyphen-ref")

    with pytest.raises(ValidationException):
        validate_credential_ref("lower_case_ref")

    with pytest.raises(ValidationException):
        validate_credential_ref("ref; rm -rf /")

    with pytest.raises(ValidationException):
        validate_credential_ref("ref/path/traversal")


def test_resolve_webcam_source():
    """Verify webcam sources resolve directly to integer device indexes."""
    res = resolve_camera_runtime_source(source_type="WEBCAM", device_index=0)
    assert res == 0

    res2 = resolve_camera_runtime_source(source_type="WEBCAM", device_index=2)
    assert res2 == 2

    with pytest.raises(ValidationException):
        resolve_camera_runtime_source(source_type="WEBCAM", device_index=None)


def test_resolve_rtsp_without_credentials():
    """Verify RTSP without credential_ref returns unmodified credential-free URL."""
    url = "rtsp://camera.internal.invalid:554/stream1"
    resolved = resolve_camera_runtime_source(source_type="RTSP", rtsp_url=url, credential_ref=None)
    assert resolved == url


def test_resolve_rtsp_with_synthetic_environment_credentials(monkeypatch):
    """Verify runtime environment credentials inject safely in memory only."""
    ref = "SYNTHETIC_TEST_CAM"
    # SAFE_SYNTHETIC_TEST_CREDENTIAL
    monkeypatch.setenv(f"PRESYN_CAMERA_{ref}_USERNAME", "synthetic_test_user")
    monkeypatch.setenv(f"PRESYN_CAMERA_{ref}_PASSWORD", "synthetic_test_p@ss#123")

    base_url = "rtsp://192.168.1.100:554/h264/ch1/main"
    resolved = resolve_camera_runtime_source(source_type="RTSP", rtsp_url=base_url, credential_ref=ref)

    assert "synthetic_test_user" in resolved
    assert "synthetic_test_p%40ss%23123" in resolved
    assert resolved.startswith("rtsp://synthetic_test_user:synthetic_test_p%40ss%23123@192.168.1.100:554/")


def test_resolve_rtsp_missing_environment_credentials(monkeypatch):
    """Verify safe error raised when credential_ref exists but env vars are missing."""
    ref = "MISSING_ENV_CAM"
    monkeypatch.delenv(f"PRESYN_CAMERA_{ref}_USERNAME", raising=False)
    monkeypatch.delenv(f"PRESYN_CAMERA_{ref}_PASSWORD", raising=False)

    with pytest.raises(CredentialsUnavailableError):
        resolve_camera_runtime_source(
            source_type="RTSP",
            rtsp_url="rtsp://192.168.1.100:554/live",
            credential_ref=ref,
        )


def test_sensitive_query_keys_rejected_in_camera_model():
    """Verify Camera model rejects sensitive credential query keys case-insensitively."""
    sensitive_urls = [
        "rtsp://192.168.1.100:554/live?token=secret123",
        "rtsp://192.168.1.100:554/live?password=secret",
        "rtsp://192.168.1.100:554/live?api_key=secretkey",
        "rtsp://192.168.1.100:554/live?secret=mysecret",
        "rtsp://192.168.1.100:554/live?PWD=secretpass",
        "rtsp://192.168.1.100:554/live?ACCESS_TOKEN=tokenval",
    ]

    for url in sensitive_urls:
        with pytest.raises(ValueError, match="RTSP URL contains a sensitive query parameter"):
            Camera(name="test_cam", rtsp_url=url, source_type="RTSP")

    # Harmless query parameters must not be rejected
    harmless_url = "rtsp://192.168.1.100:554/live?channel=1&subtype=0&codec=h264"
    cam = Camera(name="harmless_cam", rtsp_url=harmless_url, source_type="RTSP")
    assert cam.rtsp_url == harmless_url
