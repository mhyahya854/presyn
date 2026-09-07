"""enforce_finite_domain_check_constraints

Revision ID: d7327f3b3421
Revises: 71717164cbb2
Create Date: 2026-09-07 09:52:39.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'd7327f3b3421'
down_revision: Union[str, None] = '71717164cbb2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Explicitly enforce database-level CHECK constraints for finite domain statuses in SQLite
    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.create_check_constraint(
            'ck_employees_status',
            "status IN ('ACTIVE', 'INACTIVE', 'DISABLED')",
        )
        batch_op.create_check_constraint(
            'ck_employees_enrollment_status',
            "enrollment_status IN ('PENDING', 'IN_PROGRESS', 'COMPLETE', 'FAILED', 'DISABLED')",
        )

    with op.batch_alter_table('cameras', schema=None) as batch_op:
        batch_op.create_check_constraint(
            'ck_cameras_source_type',
            "source_type IN ('WEBCAM', 'RTSP')",
        )
        batch_op.create_check_constraint(
            'ck_cameras_status',
            "status IN ('OFFLINE', 'CONNECTING', 'ONLINE', 'DEGRADED', 'ERROR', 'DISABLED')",
        )

    with op.batch_alter_table('identity_verifications', schema=None) as batch_op:
        batch_op.create_check_constraint(
            'ck_identity_verifications_status',
            "status IN ('CANDIDATE', 'CONFIRMED', 'UNKNOWN', 'AMBIGUOUS', 'REJECTED', 'MANUAL_REVIEW')",
        )

    with op.batch_alter_table('presence_sessions', schema=None) as batch_op:
        batch_op.create_check_constraint(
            'ck_presence_sessions_status',
            "status IN ('VISIBLE', 'TEMPORARILY_LOST', 'LEFT_MONITORED_ZONE', 'RETURNED', 'SESSION_CLOSED')",
        )

    with op.batch_alter_table('activity_segments', schema=None) as batch_op:
        batch_op.create_check_constraint(
            'ck_activity_segments_activity_state',
            "activity_state IN ('SITTING', 'STANDING', 'WALKING', 'UNKNOWN')",
        )

    with op.batch_alter_table('unknown_people', schema=None) as batch_op:
        batch_op.create_check_constraint(
            'ck_unknown_people_resolution_status',
            "resolution_status IN ('UNRESOLVED', 'VISITOR', 'EMPLOYEE_CORRECTION', 'DISMISSED', 'SECURITY_REVIEW')",
        )

    with op.batch_alter_table('visitors', schema=None) as batch_op:
        batch_op.create_check_constraint(
            'ck_visitors_status',
            "status IN ('EXPECTED', 'CHECKED_IN', 'CHECKED_OUT', 'CANCELLED')",
        )

    with op.batch_alter_table('manual_review_items', schema=None) as batch_op:
        batch_op.create_check_constraint(
            'ck_manual_review_items_status',
            "status IN ('PENDING', 'APPROVED', 'REJECTED', 'RECLASSIFIED')",
        )

    with op.batch_alter_table('system_events', schema=None) as batch_op:
        batch_op.create_check_constraint(
            'ck_system_events_severity',
            "severity IN ('INFO', 'WARNING', 'ERROR', 'CRITICAL')",
        )


def downgrade() -> None:
    with op.batch_alter_table('system_events', schema=None) as batch_op:
        batch_op.drop_constraint('ck_system_events_severity', type_='check')

    with op.batch_alter_table('manual_review_items', schema=None) as batch_op:
        batch_op.drop_constraint('ck_manual_review_items_status', type_='check')

    with op.batch_alter_table('visitors', schema=None) as batch_op:
        batch_op.drop_constraint('ck_visitors_status', type_='check')

    with op.batch_alter_table('unknown_people', schema=None) as batch_op:
        batch_op.drop_constraint('ck_unknown_people_resolution_status', type_='check')

    with op.batch_alter_table('activity_segments', schema=None) as batch_op:
        batch_op.drop_constraint('ck_activity_segments_activity_state', type_='check')

    with op.batch_alter_table('presence_sessions', schema=None) as batch_op:
        batch_op.drop_constraint('ck_presence_sessions_status', type_='check')

    with op.batch_alter_table('identity_verifications', schema=None) as batch_op:
        batch_op.drop_constraint('ck_identity_verifications_status', type_='check')

    with op.batch_alter_table('cameras', schema=None) as batch_op:
        batch_op.drop_constraint('ck_cameras_status', type_='check')
        batch_op.drop_constraint('ck_cameras_source_type', type_='check')

    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.drop_constraint('ck_employees_enrollment_status', type_='check')
        batch_op.drop_constraint('ck_employees_status', type_='check')
