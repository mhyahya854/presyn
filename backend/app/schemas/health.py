"""Health and Diagnostic Telemetry Response Schemas."""

from pydantic import BaseModel, Field


class DatabaseHealth(BaseModel):
    """Database connectivity and engine telemetry."""

    status: str = Field(description="Database connectivity status: connected, degraded, error")
    engine: str = Field(description="Underlying database engine dialect")


class SystemMetrics(BaseModel):
    """Hardware telemetry and process metrics."""

    cpu_percent: float = Field(description="Current host CPU utilization percentage")
    memory_percent: float = Field(description="Current host RAM utilization percentage")
    uptime_seconds: float = Field(description="Process execution uptime in seconds")


class HealthResponse(BaseModel):
    """Structured response schema for /api/v1/health endpoint."""

    status: str = Field(description="Overall platform operational status: healthy, degraded, error")
    application: str = Field(default="presyn", description="Application identifier")
    version: str = Field(default="0.1.0", description="Application semantic version")
    environment: str = Field(description="Runtime environment stage")
    database: DatabaseHealth = Field(description="Database health details")
    system: SystemMetrics = Field(description="Hardware resource utilization metrics")
