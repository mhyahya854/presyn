"""System Metadata and Configuration API Route."""

from fastapi import APIRouter, status

from backend.app.schemas.system import SystemMetadataResponse
from backend.app.services.system_health import SystemHealthService

router = APIRouter(tags=["System"])


@router.get(
    "/system",
    response_model=SystemMetadataResponse,
    status_code=status.HTTP_200_OK,
    summary="System Subsystem Metadata",
    description="Returns platform configuration, registered schema tables, and subsystem readiness states.",
)
def get_system_metadata() -> SystemMetadataResponse:
    """Return truthful platform subsystem readiness states."""
    return SystemHealthService.get_system_metadata()
