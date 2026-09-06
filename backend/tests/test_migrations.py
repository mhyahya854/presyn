"""Alembic Migration Upgrade, Downgrade, and Re-Upgrade Integration Tests."""

import os
import tempfile
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect


def test_alembic_migration_lifecycle():
    """Verify clean schema creation, rollback, and re-creation via Alembic."""
    fd, path = tempfile.mkstemp(suffix="_presyn_mig_test.db")
    os.close(fd)
    db_path = path.replace("\\", "/")

    alembic_cfg = Config("backend/alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", f"sqlite:///{db_path}")

    engine = create_engine(f"sqlite:///{db_path}")

    try:
        # 1. Upgrade to head
        command.upgrade(alembic_cfg, "head")
        inspector = inspect(engine)
        up_tables = inspector.get_table_names()
        assert "employees" in up_tables
        assert "face_templates" in up_tables
        assert "attendance_records" in up_tables
        assert len(up_tables) == 24  # 23 domain tables + alembic_version

        # 2. Downgrade to base
        command.downgrade(alembic_cfg, "base")
        inspector = inspect(engine)
        down_tables = [t for t in inspector.get_table_names() if t != "alembic_version"]
        assert len(down_tables) == 0

        # 3. Re-upgrade to head
        command.upgrade(alembic_cfg, "head")
        inspector = inspect(engine)
        reup_tables = inspector.get_table_names()
        assert len(reup_tables) == 24
        assert "employees" in reup_tables
    finally:
        engine.dispose()
        if os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                pass
