"""Unit and Integrity Tests for Camera Source Model, Secrets, and Constraints."""

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.app.db.enums import CameraSourceType, CameraStatus
from backend.app.db.models.camera import Camera


def test_webcam_representation_valid(db_session: Session):
    """Test 1: Webcam representation works with source_type=WEBCAM, device_index=0, rtsp_url=None."""
    cam = Camera(
        name="test_webcam_0",
        location="Room 101",
        source_type=CameraSourceType.WEBCAM,
        device_index=0,
        rtsp_url=None,
        status=CameraStatus.OFFLINE,
    )
    db_session.add(cam)
    db_session.flush()

    retrieved = db_session.get(Camera, cam.id)
    assert retrieved is not None
    assert retrieved.source_type == CameraSourceType.WEBCAM
    assert retrieved.device_index == 0
    assert retrieved.rtsp_url is None
    assert retrieved.status == CameraStatus.OFFLINE


def test_rtsp_representation_valid(db_session: Session):
    """Test 2: RTSP representation works with source_type=RTSP, device_index=None, rtsp_url set."""
    cam = Camera(
        name="test_rtsp_stream",
        location="Front Gate",
        source_type=CameraSourceType.RTSP,
        device_index=None,
        rtsp_url="rtsp://example.invalid/stream",
        status=CameraStatus.ONLINE,
    )
    db_session.add(cam)
    db_session.flush()

    retrieved = db_session.get(Camera, cam.id)
    assert retrieved is not None
    assert retrieved.source_type == CameraSourceType.RTSP
    assert retrieved.device_index is None
    assert retrieved.rtsp_url == "rtsp://example.invalid/stream"
    assert retrieved.status == CameraStatus.ONLINE


def test_webcam_with_rtsp_url_rejected():
    """Test 3: WEBCAM with an RTSP URL is rejected at model validation level."""
    with pytest.raises(ValueError, match="WEBCAM camera source must have a null rtsp_url"):
        Camera(
            name="invalid_webcam_with_url",
            source_type=CameraSourceType.WEBCAM,
            device_index=0,
            rtsp_url="rtsp://example.invalid/stream",
        )


def test_rtsp_with_webcam_device_index_rejected():
    """Test 4: RTSP with webcam device index is rejected at model validation level."""
    with pytest.raises(ValueError, match="RTSP camera source must have a null device_index"):
        Camera(
            name="invalid_rtsp_with_device",
            source_type=CameraSourceType.RTSP,
            device_index=1,
            rtsp_url="rtsp://example.invalid/stream",
        )


def test_rtsp_with_no_url_rejected():
    """Test 5: RTSP with no URL is rejected at model validation level."""
    with pytest.raises(ValueError, match="RTSP camera source requires a non-null rtsp_url"):
        Camera(
            name="invalid_rtsp_no_url",
            source_type=CameraSourceType.RTSP,
            device_index=None,
            rtsp_url=None,
        )


def test_webcam_with_no_device_index_rejected():
    """Test 6: Webcam with no device index is rejected at model validation level."""
    with pytest.raises(ValueError, match="WEBCAM camera source requires a non-null device_index"):
        Camera(
            name="invalid_webcam_no_index",
            source_type=CameraSourceType.WEBCAM,
            device_index=None,
            rtsp_url=None,
        )


def test_inline_rtsp_credential_rejected_without_leaking():
    """Test 7: Embedded credential URL is rejected without logging or echoing the secret."""
    # Clearly synthetic test-only placeholder credentials
    synth_secret_url = "rtsp://test_user:test_password@example.invalid/stream"

    with pytest.raises(ValueError) as exc_info:
        Camera(
            name="invalid_credential_rtsp",
            source_type=CameraSourceType.RTSP,
            device_index=None,
            rtsp_url=synth_secret_url,
        )

    err_msg = str(exc_info.value)
    assert "embedded credentials or userinfo" in err_msg
    # Crucial security assertion: verify synthetic secret is never echoed in exception string
    assert "test_user" not in err_msg
    assert "test_password" not in err_msg
    assert "@" not in err_msg


def test_credential_ref_stored_safely(db_session: Session):
    """Test 8: credential_ref can be stored without storing the actual secret."""
    cam = Camera(
        name="test_rtsp_opaque_ref",
        location="Warehouse West",
        source_type=CameraSourceType.RTSP,
        device_index=None,
        rtsp_url="rtsp://example.invalid/live",
        credential_ref="MAIN_ENTRANCE_CAMERA",
        status=CameraStatus.OFFLINE,
    )
    db_session.add(cam)
    db_session.flush()

    retrieved = db_session.get(Camera, cam.id)
    assert retrieved is not None
    assert retrieved.credential_ref == "MAIN_ENTRANCE_CAMERA"
    assert retrieved.rtsp_url == "rtsp://example.invalid/live"


def test_database_check_constraint_enforcement(db_session: Session):
    """Test database-level CHECK constraint (chk_camera_source_consistency)."""
    # Attempt raw insert violating consistency: WEBCAM with rtsp_url
    with pytest.raises(IntegrityError):
        db_session.execute(
            text(
                "INSERT INTO cameras (name, source_type, device_index, rtsp_url, is_active, target_fps, reconnect_delay, status, created_at, updated_at) "
                "VALUES ('raw_bad_cam', 'WEBCAM', 0, 'rtsp://example.invalid/bad', 1, 5, 5, 'OFFLINE', '2026-09-06 00:00:00', '2026-09-06 00:00:00')"
            )
        )
        db_session.flush()
