"""Integration Tests for Health and System API Endpoints."""

from unittest.mock import MagicMock
from fastapi.testclient import TestClient

from backend.app.core.config import settings
from backend.app.schemas.health import HealthResponse
from backend.app.schemas.system import SystemMetadataResponse
from backend.app.services.system_health import SystemHealthService


def test_root_endpoint(client: TestClient):
    """Verify minimal service metadata on root path."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["application"] == "Presyn"
    assert data["status"] == "running"
    assert "version" in data


def test_health_endpoint_success(client: TestClient):
    """Verify /api/v1/health returns 200 and passes Pydantic schema validation."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()

    # Validate against Pydantic schema
    health = HealthResponse(**data)
    assert health.status == "healthy"
    assert health.application == "presyn"
    assert health.database.status == "connected"
    assert health.database.engine == "sqlite"
    assert health.system.memory_percent >= 0.0
    assert health.system.uptime_seconds >= 0.0


def test_health_endpoint_db_failure():
    """Verify health service truthfully reports degraded when database probe fails."""
    mock_db = MagicMock()
    mock_db.execute.side_effect = Exception("Simulated SQLite connection loss")
    mock_db.bind.dialect.name = "sqlite"

    health = SystemHealthService.get_health(mock_db)
    assert health.status == "degraded"
    assert health.database.status == "error"


def test_system_endpoint_success(client: TestClient):
    """Verify /api/v1/system returns truthful readiness metadata and all 23 tables."""
    response = client.get("/api/v1/system")
    assert response.status_code == 200
    data = response.json()

    # Validate against Pydantic schema
    system_meta = SystemMetadataResponse(**data)
    assert system_meta.application == "presyn"
    assert system_meta.registered_tables == 23
    assert system_meta.subsystems.camera_ingestion == "not_implemented"
    assert system_meta.subsystems.face_detection == "not_implemented"
    assert system_meta.subsystems.face_recognition == "not_implemented"
    assert system_meta.subsystems.person_tracking == "not_implemented"
    assert system_meta.subsystems.activity_estimation == "not_implemented"
    assert system_meta.feature_flags.enable_mask_detection is False


def test_no_secrets_exposed_in_api(client: TestClient):
    """Verify responses do not leak sensitive configuration, tokens, or paths."""
    for path in ["/", "/api/v1/health", "/api/v1/system"]:
        response = client.get(path)
        content = response.text.lower()
        assert settings.SECRET_KEY.lower() not in content
        assert "password" not in content
        assert "token" not in content


def test_no_camera_credentials_in_health_system_endpoints(client: TestClient, db_session):
    """Verify health and system endpoints do not expose rtsp_url, credential_ref, or secret material."""
    from backend.app.db.enums import CameraSourceType, CameraStatus
    from backend.app.db.models.camera import Camera

    # Populate camera with stream URL and credential reference in DB
    cam = Camera(
        name="secure_perimeter_cam",
        source_type=CameraSourceType.RTSP,
        device_index=None,
        rtsp_url="rtsp://example.invalid/secure_feed",
        credential_ref="MAIN_GATE_OPAQUE_SECRET_REF",
        status=CameraStatus.OFFLINE,
    )
    db_session.add(cam)
    db_session.flush()

    for path in ["/", "/api/v1/health", "/api/v1/system"]:
        response = client.get(path)
        assert response.status_code == 200
        raw_text = response.text
        assert "rtsp_url" not in raw_text
        assert "credential_ref" not in raw_text
        assert "MAIN_GATE_OPAQUE_SECRET_REF" not in raw_text
        assert "example.invalid" not in raw_text
        assert "secure_feed" not in raw_text

