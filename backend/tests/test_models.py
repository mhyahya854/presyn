"""Unit and Relational Integrity Tests for V1 Domain Models."""

from datetime import datetime, timezone
import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.app.db.base import Base
from backend.app.db.models import (
    Department,
    Employee,
    FaceTemplate,
    AttendanceRecord,
    ModelVersion,
)


def test_table_metadata_inventory():
    """Verify exact count and catalog of all 23 domain entities."""
    expected_tables = {
        "departments",
        "employees",
        "face_templates",
        "cameras",
        "zones",
        "tracks",
        "identity_verifications",
        "presence_sessions",
        "activity_segments",
        "attendance_records",
        "attendance_corrections",
        "unknown_people",
        "unknown_events",
        "visitors",
        "visitor_events",
        "manual_review_items",
        "expression_events",
        "system_events",
        "settings",
        "users_admins",
        "roles",
        "audit_logs",
        "model_versions",
    }
    actual_tables = set(Base.metadata.tables.keys())
    assert actual_tables == expected_tables
    assert len(actual_tables) == 23


def test_sqlite_foreign_key_enforcement(db_session: Session):
    """Verify SQLite foreign key pragma rejects orphan relational records."""
    # Attempt inserting employee referencing nonexistent department id 99999
    invalid_employee = Employee(
        department_id=99999,
        employee_number="SYNTH-EMP-ERR",
        first_name="Synthetic",
        last_name="Test",
    )
    db_session.add(invalid_employee)
    with pytest.raises(IntegrityError):
        db_session.flush()


def test_attendance_date_uniqueness_constraint(db_session: Session):
    """Verify arrival deduplication constraint prevents duplicate arrivals on same date."""
    dept = Department(name="Synthetic Engineering", code="SYNTH-ENG")
    db_session.add(dept)
    db_session.flush()

    emp = Employee(
        department_id=dept.id,
        employee_number="SYNTH-EMP-001",
        first_name="Synthetic",
        last_name="User",
    )
    db_session.add(emp)
    db_session.flush()

    now = datetime.now(timezone.utc)
    rec1 = AttendanceRecord(
        employee_id=emp.id,
        date="2026-09-06",
        arrival_time=now,
    )
    db_session.add(rec1)
    db_session.flush()

    # Attempt inserting second record for same employee and date
    rec2 = AttendanceRecord(
        employee_id=emp.id,
        date="2026-09-06",
        arrival_time=now,
    )
    db_session.add(rec2)
    with pytest.raises(IntegrityError):
        db_session.flush()


def test_cascade_deletion_face_templates(db_session: Session):
    """Verify deleting an employee removes their associated biometric templates."""
    emp = Employee(
        employee_number="SYNTH-EMP-DEL",
        first_name="Delete",
        last_name="Test",
    )
    db_session.add(emp)
    db_session.flush()

    # Synthetic non-biometric byte vector for test
    synthetic_vector = b"\x00" * 2048  # 512 float32 bytes
    template = FaceTemplate(
        employee_id=emp.id,
        vector_512d=synthetic_vector,
        view_type="FRONT_UNMASKED",
        quality_score=95.0,
    )
    db_session.add(template)
    db_session.flush()

    template_id = template.id
    db_session.delete(emp)
    db_session.flush()

    # Verify template was cascade deleted
    remaining = db_session.get(FaceTemplate, template_id)
    assert remaining is None


def test_model_version_sha256_standard(db_session: Session):
    """Verify model_version stores SHA-256 integrity hash standard."""
    mv = ModelVersion(
        module_name="scrfd_face_detector",
        model_file="scrfd_500m_bnkps.onnx",
        sha256_hash="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        is_active=True,
    )
    db_session.add(mv)
    db_session.flush()
    assert len(mv.sha256_hash) == 64
