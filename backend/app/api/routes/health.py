"""Health and Readiness Diagnostic API Route."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.schemas.health import HealthResponse
from backend.app.services.system_health import SystemHealthService

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="System Health Telemetry",
    description="Returns real-time host hardware resource metrics, database connectivity, and platform health.",
)
def get_health(db: Session = Depends(get_db)) -> HealthResponse:
    """Return truthful system health diagnostics."""
    return SystemHealthService.get_health(db)
