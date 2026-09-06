"""System Health and Readiness Diagnostic Service."""

import time
import psutil
from sqlalchemy import text
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.core.logging import logger
from backend.app.db.base import Base
from backend.app.schemas.health import HealthResponse, DatabaseHealth, SystemMetrics
from backend.app.schemas.system import SystemMetadataResponse, SubsystemStatus, FeatureFlags

# Record process startup timestamp for truthful uptime calculation
PROCESS_START_TIME = time.time()


class SystemHealthService:
    """Diagnostic service gathering truthful database and host hardware metrics."""

    @staticmethod
    def get_health(db: Session) -> HealthResponse:
        """Evaluate database connectivity and host resource utilization."""
        # 1. Database Connectivity Probe
        db_status = "connected"
        engine_dialect = db.bind.dialect.name if db.bind else "unknown"

        try:
            db.execute(text("SELECT 1"))
        except Exception as exc:
            logger.error("Database health probe failed: %s", exc)
            db_status = "error"

        # 2. Host Telemetry via psutil
        try:
            cpu_percent = psutil.cpu_percent(interval=None)
            memory_info = psutil.virtual_memory()
            memory_percent = memory_info.percent
        except Exception as exc:
            logger.warning("Failed to collect psutil metrics: %s", exc)
            cpu_percent = 0.0
            memory_percent = 0.0

        uptime_seconds = round(time.time() - PROCESS_START_TIME, 2)
        overall_status = "healthy" if db_status == "connected" else "degraded"

        return HealthResponse(
            status=overall_status,
            application="presyn",
            version="0.1.0",
            environment=settings.ENVIRONMENT,
            database=DatabaseHealth(
                status=db_status,
                engine=engine_dialect,
            ),
            system=SystemMetrics(
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                uptime_seconds=uptime_seconds,
            ),
        )

    @staticmethod
    def get_system_metadata() -> SystemMetadataResponse:
        """Return truthful subsystem readiness and platform feature flags."""
        table_count = len(Base.metadata.tables)

        return SystemMetadataResponse(
            application="presyn",
            version="0.1.0",
            environment=settings.ENVIRONMENT,
            target_hardware="Intel Core i7-1355U / Modern x86_64 CPU",
            registered_tables=table_count,
            subsystems=SubsystemStatus(
                camera_ingestion="not_implemented",  # Phase 02
                face_detection="not_implemented",    # Phase 03
                face_recognition="not_implemented",  # Phase 05
                person_tracking="not_implemented",   # Phase 10
                activity_estimation="not_implemented", # Phase 12
                mask_detection="enabled" if settings.ENABLE_MASK_DETECTION else "disabled",
                liveness_probe="enabled" if settings.ENABLE_LIVENESS_CHECK else "disabled",
                expression_trends="enabled" if settings.ENABLE_EXPRESSION_TRENDS else "disabled",
            ),
            feature_flags=FeatureFlags(
                enable_mask_detection=settings.ENABLE_MASK_DETECTION,
                enable_liveness_check=settings.ENABLE_LIVENESS_CHECK,
                enable_expression_trends=settings.ENABLE_EXPRESSION_TRENDS,
            ),
        )
