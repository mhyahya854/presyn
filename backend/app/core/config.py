"""Typed Application Settings for Presyn Platform."""

from typing import List, Union
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Presyn Application Configuration Settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # Server and Environment
    ENVIRONMENT: str = Field(default="development", description="Environment stage: development, testing, production")
    HOST: str = Field(default="127.0.0.1", description="Server bind host")
    PORT: int = Field(default=8000, description="Server bind port")
    LOG_LEVEL: str = Field(default="INFO", description="Application log level")
    CORS_ORIGINS: Union[str, List[str]] = Field(
        default="http://localhost:5173,http://127.0.0.1:5173",
        description="Allowed CORS origin URLs (comma-separated or list)",
    )

    # Security and Tokens
    SECRET_KEY: str = Field(
        default="change-this-insecure-key-before-production-deployment-min32chars",
        description="Secret key for security signing and authentication",
    )
    ALGORITHM: str = Field(default="HS256", description="Cryptographic signing algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=480, description="Access token expiration in minutes")

    # Database
    DATABASE_URL: str = Field(
        default="sqlite:///./data/presyn.db",
        description="SQLAlchemy database connection URI",
    )

    # Ingestion and Inference Defaults (Configured for future phases)
    PROCESSING_FPS: int = Field(default=5, description="Target processing frame rate per camera")
    FRAME_WIDTH: int = Field(default=1280, description="Target frame width")
    FRAME_HEIGHT: int = Field(default=720, description="Target frame height")
    CAMERA_RECONNECT_INTERVAL_SECONDS: int = Field(default=2, description="Initial reconnect delay in seconds")
    CAMERA_RECONNECT_INITIAL_SECONDS: int = Field(default=2, description="Initial reconnect backoff delay in seconds")
    CAMERA_RECONNECT_MAX_SECONDS: int = Field(default=30, description="Maximum reconnect backoff delay cap in seconds")
    CAMERA_PREVIEW_FPS: int = Field(default=10, description="Target preview frame rate for browser streaming")
    CAMERA_JPEG_QUALITY: int = Field(default=75, description="JPEG quality for live preview encoding (1-100)")
    CAMERA_PREVIEW_MAX_WIDTH: int = Field(default=640, description="Maximum width for browser preview JPEG encoding")
    CAMERA_READ_FAILURE_THRESHOLD: int = Field(default=5, description="Consecutive read failure tolerance before reconnect")
    CAMERA_MAX_RECONNECT_ATTEMPTS: int = Field(default=10, description="Maximum camera reconnect attempts")

    # Face Quality and Matching Thresholds
    FACE_MIN_SIZE_PX: int = Field(default=48, description="Minimum face size bounding box in pixels")
    FACE_BLUR_THRESHOLD: float = Field(default=60.0, description="Laplacian variance blur threshold")
    FACE_BRIGHTNESS_MIN: float = Field(default=40.0, description="Minimum illumination brightness score")
    FACE_BRIGHTNESS_MAX: float = Field(default=220.0, description="Maximum illumination brightness score")
    FACE_SIMILARITY_THRESHOLD: float = Field(default=0.65, description="Cosine similarity threshold for top-1 match")
    FACE_MARGIN_THRESHOLD: float = Field(default=0.10, description="Top-1 to Top-2 candidate margin threshold")
    FACE_MAX_TEMPLATES_PER_EMPLOYEE: int = Field(default=50, description="Maximum stored templates per employee")
    VERIFICATION_WINDOW_SECONDS: float = Field(default=2.0, description="Multi-frame verification window duration")
    VERIFICATION_MIN_VOTES: int = Field(default=5, description="Minimum agreeing votes required for confirmation")
    INCREMENTAL_LEARNING_THRESHOLD: float = Field(default=0.82, description="Conservative incremental learning score")
    INCREMENTAL_LEARNING_MARGIN: float = Field(default=0.15, description="Incremental learning candidate margin")

    # Tracking Configuration
    TRACK_LOST_TIMEOUT_SECONDS: float = Field(default=3.0, description="ByteTrack track lost timeout duration")
    PRESENCE_TEMPORARILY_LOST_SECONDS: float = Field(default=15.0, description="Presence temporarily lost timeout")

    # Optional Feature Flags (All Default to False)
    ENABLE_MASK_DETECTION: bool = Field(default=False, description="Enable optional mask detection module")
    ENABLE_LIVENESS_CHECK: bool = Field(default=False, description="Enable optional liveness check module")
    ENABLE_EXPRESSION_TRENDS: bool = Field(default=False, description="Enable optional expression trends module")

    # Visitor and Security Policy
    DEFAULT_VISITOR_MODE: bool = Field(default=False, description="Initial system-wide visitor mode state")
    UNKNOWN_ALERT_COOLDOWN_SECONDS: int = Field(default=60, description="Alert cooldown period for unknown sightings")

    # Retention Policies (Days)
    EVENT_RETENTION_DAYS: int = Field(default=90, description="Retention duration for presence and system events")
    AUDIT_LOG_RETENTION_DAYS: int = Field(default=365, description="Retention duration for immutable audit logs")
    SNAPSHOT_RETENTION_DAYS: int = Field(default=7, description="Retention duration for temporary thumbnail crops")

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS_ORIGINS into a clean list of allowed string origins."""
        if isinstance(self.CORS_ORIGINS, list):
            return self.CORS_ORIGINS
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


settings = Settings()
