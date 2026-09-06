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
