from enum import Enum


class CameraSourceType(str, Enum):
    WEBCAM = "WEBCAM"
    RTSP = "RTSP"


class CameraStatus(str, Enum):
    OFFLINE = "OFFLINE"
    CONNECTING = "CONNECTING"
    ONLINE = "ONLINE"
    DEGRADED = "DEGRADED"
    ERROR = "ERROR"
    DISABLED = "DISABLED"


class EmployeeStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DISABLED = "DISABLED"


class EnrollmentStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"
    DISABLED = "DISABLED"


class PresenceStatus(str, Enum):
    VISIBLE = "VISIBLE"
    TEMPORARILY_LOST = "TEMPORARILY_LOST"
    LEFT_MONITORED_ZONE = "LEFT_MONITORED_ZONE"
    RETURNED = "RETURNED"
    SESSION_CLOSED = "SESSION_CLOSED"


class ActivityState(str, Enum):
    SITTING = "SITTING"
    STANDING = "STANDING"
    WALKING = "WALKING"
    UNKNOWN = "UNKNOWN"


class RecognitionStatus(str, Enum):
    CANDIDATE = "CANDIDATE"
    CONFIRMED = "CONFIRMED"
    UNKNOWN = "UNKNOWN"
    AMBIGUOUS = "AMBIGUOUS"
    REJECTED = "REJECTED"
    MANUAL_REVIEW = "MANUAL_REVIEW"


class ReviewStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    RECLASSIFIED = "RECLASSIFIED"


class VisitorStatus(str, Enum):
    EXPECTED = "EXPECTED"
    CHECKED_IN = "CHECKED_IN"
    CHECKED_OUT = "CHECKED_OUT"
    CANCELLED = "CANCELLED"


class UnknownResolutionStatus(str, Enum):
    UNRESOLVED = "UNRESOLVED"
    VISITOR = "VISITOR"
    EMPLOYEE_CORRECTION = "EMPLOYEE_CORRECTION"
    DISMISSED = "DISMISSED"
    SECURITY_REVIEW = "SECURITY_REVIEW"


class EventSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
