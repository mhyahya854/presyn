"""System Metadata and Subsystem Readiness Schemas."""

from pydantic import BaseModel, Field


class SubsystemStatus(BaseModel):
    """Truthful readiness state of platform modules."""

    camera_ingestion: str = Field(description="Camera video ingestion subsystem status")
    face_detection: str = Field(description="SCRFD face detection model status")
    face_recognition: str = Field(description="ArcFace embedding matching subsystem status")
    person_tracking: str = Field(description="ByteTrack spatial tracking subsystem status")
    activity_estimation: str = Field(description="Physical activity state estimator status")
    mask_detection: str = Field(description="Optional mask classification module status")
    liveness_probe: str = Field(description="Optional liveness and anti-spoof module status")
    expression_trends: str = Field(description="Optional facial expression analysis status")


class FeatureFlags(BaseModel):
    """Active feature flag configuration values."""

    enable_mask_detection: bool = Field(description="Whether mask detection is enabled")
    enable_liveness_check: bool = Field(description="Whether liveness checking is enabled")
    enable_expression_trends: bool = Field(description="Whether expression trend analysis is enabled")


class SystemMetadataResponse(BaseModel):
    """Structured response schema for /api/v1/system endpoint."""

    application: str = Field(default="presyn", description="Application platform name")
    version: str = Field(default="0.1.0", description="Semantic platform release version")
    environment: str = Field(description="Current deployment environment")
    target_hardware: str = Field(default="Intel Core i7-1355U / Modern x86_64 CPU", description="Architecture target")
    registered_tables: int = Field(description="Count of active relational schema tables")
    subsystems: SubsystemStatus = Field(description="Truthful module operational status")
    feature_flags: FeatureFlags = Field(description="Current platform feature flags")
