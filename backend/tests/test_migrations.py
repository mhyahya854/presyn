"""Alembic Migration Upgrade, Downgrade, Path A, Path B, and Lifecycle Integration Tests."""

import os
import tempfile
from alembic import command
from alembic.config import Config
import pytest
from sqlalchemy import create_engine, inspect, text


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

    # 1. Upgrade specifically to previous head: fc17a53ea5e7
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

    # 5. Downgrade one revision (back to fc17a53ea5e7)
    command.downgrade(cfg, "-1")

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT id, name, rtsp_url, status FROM cameras WHERE name = :name"),
            {"name": "synth-cam-pre-correction"},
        ).fetchone()
        assert result is not None
        assert result[1] == "synth-cam-pre-correction"
        assert result[2] == "rtsp://example.invalid/live"
        assert result[3] == "OFFLINE"

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
