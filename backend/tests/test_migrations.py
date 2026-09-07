"""Alembic Migration Upgrade, Downgrade, Path A, B, C, Parity, and Direct SQL Constraint Tests."""

import os
import tempfile
from alembic import command
from alembic.config import Config
import pytest
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import IntegrityError

from backend.app.db.base import Base


@pytest.fixture
def temp_db_config():
    """Create a temporary SQLite database and Alembic config."""
    fd, path = tempfile.mkstemp(suffix="_presyn_mig_test.db")
    os.close(fd)
    db_path = path.replace("\\", "/")
    db_url = f"sqlite:///{db_path}"

    cfg = Config("backend/alembic.ini")
    cfg.set_main_option("sqlalchemy.url", db_url)

    engine = create_engine(db_url)

    yield cfg, engine, path

    engine.dispose()
    if os.path.exists(path):
        try:
            os.remove(path)
        except OSError:
            pass


def test_migration_lifecycle_base_head_base_head(temp_db_config):
    """Verify clean full lifecycle: base -> head -> base -> head."""
    cfg, engine, _ = temp_db_config

    # 1. Base to Head
    command.upgrade(cfg, "head")
    inspector = inspect(engine)
    up_tables = set(inspector.get_table_names())
    assert "employees" in up_tables
    assert "cameras" in up_tables
    assert "face_templates" in up_tables
    assert len(up_tables) == 24  # 23 domain tables + alembic_version

    camera_cols = {col["name"] for col in inspector.get_columns("cameras")}
    assert "source_type" in camera_cols
    assert "device_index" in camera_cols
    assert "credential_ref" in camera_cols
    assert "rtsp_url" in camera_cols

    # 2. Head to Base
    command.downgrade(cfg, "base")
    inspector = inspect(engine)
    down_tables = [t for t in inspector.get_table_names() if t != "alembic_version"]
    assert len(down_tables) == 0

    # 3. Re-upgrade Base to Head
    command.upgrade(cfg, "head")
    inspector = inspect(engine)
    reup_tables = set(inspector.get_table_names())
    assert len(reup_tables) == 24
    assert "cameras" in reup_tables


def test_migration_path_a_empty_to_new_head(temp_db_config):
    """PATH A: Empty DB upgraded directly to new head."""
    cfg, engine, _ = temp_db_config

    command.upgrade(cfg, "head")
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert len(tables) == 24

    cols = {col["name"]: col for col in inspector.get_columns("cameras")}
    assert cols["source_type"]["nullable"] is False
    assert cols["rtsp_url"]["nullable"] is True
    assert cols["device_index"]["nullable"] is True
    assert cols["credential_ref"]["nullable"] is True


def test_migration_path_b_old_head_to_new_head_and_downgrade(temp_db_config):
    """PATH B: Empty DB -> upgrade fc17a53ea5e7 -> insert pre-correction row -> upgrade head -> downgrade -> re-upgrade."""
    cfg, engine, _ = temp_db_config

    # 1. Upgrade specifically to initial v1 head: fc17a53ea5e7
    command.upgrade(cfg, "fc17a53ea5e7")

    # 2. Insert representative safe synthetic pre-correction rows (no real cameras, no real credentials)
    with engine.connect() as conn:
        conn.execute(
            text(
                "INSERT INTO cameras (name, location, rtsp_url, is_active, target_fps, reconnect_delay, status, created_at, updated_at) "
                "VALUES (:name, :location, :rtsp_url, :is_active, :target_fps, :reconnect_delay, :status, :created_at, :updated_at)"
            ),
            {
                "name": "synth-cam-pre-correction",
                "location": "Synthetic Test Lab",
                "rtsp_url": "rtsp://example.invalid/live",
                "is_active": 1,
                "target_fps": 5,
                "reconnect_delay": 5,
                "status": "OFFLINE",
                "created_at": "2026-09-06 00:00:00",
                "updated_at": "2026-09-06 00:00:00",
            },
        )
        conn.commit()

    # 3. Upgrade to new head
    command.upgrade(cfg, "head")

    # 4. Verify pre-existing row was safely preserved and automatically classified as RTSP
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT id, name, source_type, device_index, rtsp_url, credential_ref, status FROM cameras WHERE name = :name"),
            {"name": "synth-cam-pre-correction"},
        ).fetchone()

        assert result is not None
        assert result[1] == "synth-cam-pre-correction"
        assert result[2] == "RTSP"
        assert result[3] is None  # device_index is NULL for RTSP
        assert result[4] == "rtsp://example.invalid/live"
        assert result[5] is None  # credential_ref is NULL
        assert result[6] == "OFFLINE"

    # 5. Downgrade one revision (back to 71717164cbb2)
    command.downgrade(cfg, "-1")

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT id, name, source_type, rtsp_url FROM cameras WHERE name = :name"),
            {"name": "synth-cam-pre-correction"},
        ).fetchone()
        assert result is not None
        assert result[1] == "synth-cam-pre-correction"
        assert result[2] == "RTSP"

    # 6. Upgrade to new head again
    command.upgrade(cfg, "head")

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT id, name, source_type, device_index, rtsp_url FROM cameras WHERE name = :name"),
            {"name": "synth-cam-pre-correction"},
        ).fetchone()
        assert result is not None
        assert result[2] == "RTSP"
        assert result[4] == "rtsp://example.invalid/live"


def test_migration_path_c_previous_correction_to_new_head(temp_db_config):
    """PATH C: Upgrade 71717164cbb2 -> upgrade d7327f3b3421 (new head) -> downgrade -> re-upgrade."""
    cfg, engine, _ = temp_db_config

    command.upgrade(cfg, "71717164cbb2")

    with engine.connect() as conn:
        conn.execute(
            text(
                "INSERT INTO employees (employee_number, first_name, last_name, status, enrollment_status, created_at, updated_at) "
                "VALUES ('E-PATH-C', 'Synth', 'User', 'ACTIVE', 'COMPLETE', '2026-09-06 00:00:00', '2026-09-06 00:00:00')"
            )
        )
        conn.commit()

    # Upgrade to head (d7327f3b3421)
    command.upgrade(cfg, "head")

    with engine.connect() as conn:
        row = conn.execute(
            text("SELECT employee_number, status, enrollment_status FROM employees WHERE employee_number = 'E-PATH-C'")
        ).fetchone()
        assert row is not None
        assert row[1] == "ACTIVE"
        assert row[2] == "COMPLETE"

    # Downgrade 1 revision back to 71717164cbb2
    command.downgrade(cfg, "-1")

    # Re-upgrade to head
    command.upgrade(cfg, "head")


def test_migrated_head_direct_sql_invalid_enums_rejected(temp_db_config):
    """Verify direct SQL inserts bypassing ORM fail on Alembic-migrated database due to SQLite CHECK constraints."""
    cfg, engine, _ = temp_db_config

    command.upgrade(cfg, "head")

    # 1. Invalid employee status
    with engine.connect() as conn:
        with pytest.raises(IntegrityError):
            conn.execute(
                text(
                    "INSERT INTO employees (employee_number, first_name, last_name, status, enrollment_status, created_at, updated_at) "
                    "VALUES ('E-INVALID-1', 'A', 'B', 'INVALID_STATUS', 'PENDING', '2026-09-06 00:00:00', '2026-09-06 00:00:00')"
                )
            )

    # 2. Invalid camera status
    with engine.connect() as conn:
        with pytest.raises(IntegrityError):
            conn.execute(
                text(
                    "INSERT INTO cameras (name, source_type, device_index, rtsp_url, is_active, target_fps, reconnect_delay, status, created_at, updated_at) "
                    "VALUES ('cam_bad_status', 'WEBCAM', 0, NULL, 1, 5, 5, 'INVALID_STATUS', '2026-09-06 00:00:00', '2026-09-06 00:00:00')"
                )
            )

    # 3. Invalid visitor status
    with engine.connect() as conn:
        with pytest.raises(IntegrityError):
            conn.execute(
                text(
                    "INSERT INTO visitors (full_name, status, created_at, updated_at) "
                    "VALUES ('Invalid Visitor', 'INVALID_STATUS', '2026-09-06 00:00:00', '2026-09-06 00:00:00')"
                )
            )

    # 4. Invalid system event severity
    with engine.connect() as conn:
        with pytest.raises(IntegrityError):
            conn.execute(
                text(
                    "INSERT INTO system_events (event_type, severity, component, message, timestamp) "
                    "VALUES ('SYS_TEST', 'INVALID_SEVERITY', 'core', 'msg', '2026-09-06 00:00:00')"
                )
            )


def test_migrated_head_direct_sql_invalid_camera_source_rejected(temp_db_config):
    """Verify direct SQL with invalid camera source combinations fails due to chk_camera_source_consistency."""
    cfg, engine, _ = temp_db_config

    command.upgrade(cfg, "head")

    # WEBCAM with rtsp_url
    with engine.connect() as conn:
        with pytest.raises(IntegrityError):
            conn.execute(
                text(
                    "INSERT INTO cameras (name, source_type, device_index, rtsp_url, is_active, target_fps, reconnect_delay, status, created_at, updated_at) "
                    "VALUES ('cam_bad_combo', 'WEBCAM', 0, 'rtsp://example.invalid/feed', 1, 5, 5, 'OFFLINE', '2026-09-06 00:00:00', '2026-09-06 00:00:00')"
                )
            )

    # RTSP with device_index
    with engine.connect() as conn:
        with pytest.raises(IntegrityError):
            conn.execute(
                text(
                    "INSERT INTO cameras (name, source_type, device_index, rtsp_url, is_active, target_fps, reconnect_delay, status, created_at, updated_at) "
                    "VALUES ('cam_bad_combo2', 'RTSP', 1, 'rtsp://example.invalid/feed', 1, 5, 5, 'OFFLINE', '2026-09-06 00:00:00', '2026-09-06 00:00:00')"
                )
            )


def test_metadata_vs_migration_parity(temp_db_config):
    """Verify semantic parity between Base.metadata schema constraints and Alembic HEAD schema."""
    cfg, engine, _ = temp_db_config

    command.upgrade(cfg, "head")

    # Extract all table DDL definitions from SQLite master
    with engine.connect() as conn:
        sqlite_ddl = {
            row[0]: row[1]
            for row in conn.execute(
                text("SELECT name, sql FROM sqlite_master WHERE type='table' AND name != 'alembic_version'")
            ).fetchall()
        }

    # Verify key CHECK constraints exist in the migrated tables
    assert "chk_camera_source_consistency" in sqlite_ddl["cameras"]
    assert "ck_cameras_source_type" in sqlite_ddl["cameras"]
    assert "ck_cameras_status" in sqlite_ddl["cameras"]
    assert "ck_employees_status" in sqlite_ddl["employees"]
    assert "ck_employees_enrollment_status" in sqlite_ddl["employees"]
    assert "ck_identity_verifications_status" in sqlite_ddl["identity_verifications"]
    assert "ck_presence_sessions_status" in sqlite_ddl["presence_sessions"]
    assert "ck_activity_segments_activity_state" in sqlite_ddl["activity_segments"]
    assert "ck_unknown_people_resolution_status" in sqlite_ddl["unknown_people"]
    assert "ck_visitors_status" in sqlite_ddl["visitors"]
    assert "ck_manual_review_items_status" in sqlite_ddl["manual_review_items"]
    assert "ck_system_events_severity" in sqlite_ddl["system_events"]

    # All 23 domain models exist in both metadata and migrated database
    metadata_tables = set(Base.metadata.tables.keys())
    migrated_tables = set(sqlite_ddl.keys())
    assert metadata_tables == migrated_tables
    assert len(migrated_tables) == 23
