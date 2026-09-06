"""Presyn Domain Model Registry (23 Entities)."""

from backend.app.db.models.department import Department
from backend.app.db.models.employee import Employee
from backend.app.db.models.face_template import FaceTemplate
from backend.app.db.models.camera import Camera
from backend.app.db.models.zone import Zone
from backend.app.db.models.track import Track
from backend.app.db.models.identity_verification import IdentityVerification
from backend.app.db.models.presence_session import PresenceSession
from backend.app.db.models.activity_segment import ActivitySegment
from backend.app.db.models.attendance_record import AttendanceRecord
from backend.app.db.models.attendance_correction import AttendanceCorrection
from backend.app.db.models.unknown_person import UnknownPerson
from backend.app.db.models.unknown_event import UnknownEvent
from backend.app.db.models.visitor import Visitor
from backend.app.db.models.visitor_event import VisitorEvent
from backend.app.db.models.manual_review_item import ManualReviewItem
from backend.app.db.models.expression_event import ExpressionEvent
from backend.app.db.models.system_event import SystemEvent
from backend.app.db.models.setting import Setting
from backend.app.db.models.user import UserAdmin
from backend.app.db.models.role import Role
from backend.app.db.models.audit_log import AuditLog
from backend.app.db.models.model_version import ModelVersion

__all__ = [
    "Department",
    "Employee",
    "FaceTemplate",
    "Camera",
    "Zone",
    "Track",
    "IdentityVerification",
    "PresenceSession",
    "ActivitySegment",
    "AttendanceRecord",
    "AttendanceCorrection",
    "UnknownPerson",
    "UnknownEvent",
    "Visitor",
    "VisitorEvent",
    "ManualReviewItem",
    "ExpressionEvent",
    "SystemEvent",
    "Setting",
    "UserAdmin",
    "Role",
    "AuditLog",
    "ModelVersion",
]
