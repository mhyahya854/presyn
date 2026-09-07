"""Unit and Relational Tests for Finite Domain Status Enums."""

from datetime import datetime, timezone
import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError, StatementError
from sqlalchemy.orm import Session

from backend.app.db.enums import (
    ActivityState,
    CameraSourceType,
    CameraStatus,
    EmployeeStatus,
    EnrollmentStatus,
    EventSeverity,
    PresenceStatus,
    RecognitionStatus,
    ReviewStatus,
    UnknownResolutionStatus,
    VisitorStatus,
)
from backend.app.db.models import (
    ActivitySegment,
    Camera,
    Employee,
    IdentityVerification,
    ManualReviewItem,
    PresenceSession,
    SystemEvent,
    Track,
    UnknownPerson,
    Visitor,
)


def test_valid_enum_instantiation_and_persistence(db_session: Session):
    """Verify models instantiate and persist valid enum values cleanly."""
    emp = Employee(
        employee_number="SYNTH-ENUM-01",
        first_name="Alice",
        last_name="Enum",
        status=EmployeeStatus.ACTIVE,
        enrollment_status=EnrollmentStatus.COMPLETE,
    )
    db_session.add(emp)
    db_session.flush()

    cam = Camera(
        name="test_enum_cam",
        source_type=CameraSourceType.WEBCAM,
        device_index=0,
        status=CameraStatus.ONLINE,
    )
    db_session.add(cam)
    db_session.flush()

    track = Track(
        camera_id=cam.id,
        track_id=1,
        started_at=datetime.now(timezone.utc),
    )
    db_session.add(track)
    db_session.flush()

    ident = IdentityVerification(
        track_id=track.id,
        confidence=0.98,
        vote_count=5,
        status=RecognitionStatus.CONFIRMED,
        verified_at=datetime.now(timezone.utc),
    )
    db_session.add(ident)

    sess = PresenceSession(
        employee_id=emp.id,
        camera_id=cam.id,
        first_seen=datetime.now(timezone.utc),
        last_seen=datetime.now(timezone.utc),
        status=PresenceStatus.VISIBLE,
    )
    db_session.add(sess)
    db_session.flush()

    act = ActivitySegment(
        session_id=sess.id,
        activity_state=ActivityState.SITTING,
        started_at=datetime.now(timezone.utc),
    )
    db_session.add(act)

    unk = UnknownPerson(
        first_seen=datetime.now(timezone.utc),
        last_seen=datetime.now(timezone.utc),
        resolution_status=UnknownResolutionStatus.UNRESOLVED,
    )
    db_session.add(unk)

    vis = Visitor(
        full_name="Bob Visitor",
        status=VisitorStatus.CHECKED_IN,
    )
    db_session.add(vis)

    rev = ManualReviewItem(
        item_type="AMBIGUOUS_MATCH",
        candidate_data_json="{}",
        status=ReviewStatus.PENDING,
    )
    db_session.add(rev)

    evt = SystemEvent(
        event_type="HEALTH_CHECK",
        severity=EventSeverity.INFO,
        component="test",
        message="test message",
        timestamp=datetime.now(timezone.utc),
    )
    db_session.add(evt)

    db_session.flush()

    # Assert retrieved enum values serialize predictably as Python enums and string values
    assert emp.status == EmployeeStatus.ACTIVE
    assert emp.status.value == "ACTIVE"
    assert emp.enrollment_status == EnrollmentStatus.COMPLETE
    assert cam.source_type == CameraSourceType.WEBCAM
    assert cam.status == CameraStatus.ONLINE
    assert ident.status == RecognitionStatus.CONFIRMED
    assert sess.status == PresenceStatus.VISIBLE
    assert act.activity_state == ActivityState.SITTING
    assert unk.resolution_status == UnknownResolutionStatus.UNRESOLVED
    assert vis.status == VisitorStatus.CHECKED_IN
    assert rev.status == ReviewStatus.PENDING
    assert evt.severity == EventSeverity.INFO


@pytest.mark.parametrize(
    "model_class,field_name,invalid_val,kwargs",
    [
        (Employee, "status", "INVALID_STATUS", {"employee_number": "E1", "first_name": "A", "last_name": "B"}),
        (Employee, "enrollment_status", "NOT_A_STATUS", {"employee_number": "E2", "first_name": "A", "last_name": "B"}),
        (Camera, "status", "EXPLODED", {"name": "C1", "source_type": CameraSourceType.WEBCAM, "device_index": 0}),
        (Visitor, "status", "LOST", {"full_name": "Visitor X"}),
        (ManualReviewItem, "status", "UNKNOWN_REV", {"item_type": "T", "candidate_data_json": "{}"}),
        (SystemEvent, "severity", "CATASTROPHIC", {"event_type": "E", "component": "C", "message": "M", "timestamp": datetime.now(timezone.utc)}),
    ],
)
def test_invalid_enum_rejected_at_orm_level(db_session: Session, model_class, field_name, invalid_val, kwargs):
    """Verify ORM rejects assignment of arbitrary uncontrolled strings for finite enums."""
    kwargs[field_name] = invalid_val
    instance = model_class(**kwargs)
    db_session.add(instance)
    with pytest.raises((StatementError, ValueError, LookupError)):
        db_session.flush()


def test_database_enum_constraint_enforcement(db_session: Session):
    """Verify database-level check constraint rejects invalid enum strings from direct SQL."""
    with pytest.raises(IntegrityError):
        db_session.execute(
            text(
                "INSERT INTO employees (employee_number, first_name, last_name, status, enrollment_status, created_at, updated_at) "
                "VALUES ('RAW-EMP-ERR', 'Test', 'User', 'BOGUS_STATUS', 'PENDING', '2026-09-06 00:00:00', '2026-09-06 00:00:00')"
            )
        )
        db_session.flush()
