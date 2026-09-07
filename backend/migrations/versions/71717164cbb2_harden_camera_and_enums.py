"""harden_camera_and_enums

Revision ID: 71717164cbb2
Revises: fc17a53ea5e7
Create Date: 2026-09-06 23:41:49.279241

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '71717164cbb2'
down_revision: Union[str, None] = 'fc17a53ea5e7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Update cameras schema: add source_type, device_index, credential_ref, make rtsp_url nullable,
    # classify existing rows as RTSP, and add consistency constraint.
    with op.batch_alter_table('cameras', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                'source_type',
                sa.Enum('WEBCAM', 'RTSP', name='camerasourcetype', native_enum=False),
                nullable=False,
                server_default='RTSP',
            )
        )
        batch_op.add_column(sa.Column('device_index', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('credential_ref', sa.String(length=100), nullable=True))
        batch_op.alter_column('rtsp_url', existing_type=sa.String(length=255), nullable=True)
        batch_op.alter_column(
            'status',
            existing_type=sa.String(length=20),
            type_=sa.Enum('OFFLINE', 'CONNECTING', 'ONLINE', 'DEGRADED', 'ERROR', 'DISABLED', name='camerastatus', native_enum=False),
            nullable=False,
            server_default='OFFLINE',
        )
        batch_op.create_check_constraint(
            'chk_camera_source_consistency',
            "((source_type = 'WEBCAM' AND device_index IS NOT NULL AND rtsp_url IS NULL) OR "
            "(source_type = 'RTSP' AND device_index IS NULL AND rtsp_url IS NOT NULL))",
        )

    # 2. Update employees status and enrollment_status enums
    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.alter_column(
            'status',
            existing_type=sa.String(length=20),
            type_=sa.Enum('ACTIVE', 'INACTIVE', 'DISABLED', name='employeestatus', native_enum=False),
            nullable=False,
            server_default='ACTIVE',
        )
        batch_op.alter_column(
            'enrollment_status',
            existing_type=sa.String(length=30),
            type_=sa.Enum('PENDING', 'IN_PROGRESS', 'COMPLETE', 'FAILED', 'DISABLED', name='enrollmentstatus', native_enum=False),
            nullable=False,
            server_default='PENDING',
        )

    # 3. Update identity_verifications recognition status enum
    with op.batch_alter_table('identity_verifications', schema=None) as batch_op:
        batch_op.alter_column(
            'status',
            existing_type=sa.String(length=30),
            type_=sa.Enum('CANDIDATE', 'CONFIRMED', 'UNKNOWN', 'AMBIGUOUS', 'REJECTED', 'MANUAL_REVIEW', name='recognitionstatus', native_enum=False),
            nullable=False,
        )

    # 4. Update presence_sessions status enum
    with op.batch_alter_table('presence_sessions', schema=None) as batch_op:
        batch_op.alter_column(
            'status',
            existing_type=sa.String(length=30),
            type_=sa.Enum('VISIBLE', 'TEMPORARILY_LOST', 'LEFT_MONITORED_ZONE', 'RETURNED', 'SESSION_CLOSED', name='presencestatus', native_enum=False),
            nullable=False,
            server_default='VISIBLE',
        )

    # 5. Update activity_segments activity_state enum
    with op.batch_alter_table('activity_segments', schema=None) as batch_op:
        batch_op.alter_column(
            'activity_state',
            existing_type=sa.String(length=30),
            type_=sa.Enum('SITTING', 'STANDING', 'WALKING', 'UNKNOWN', name='activitystate', native_enum=False),
            nullable=False,
        )

    # 6. Update unknown_people resolution_status enum
    with op.batch_alter_table('unknown_people', schema=None) as batch_op:
        batch_op.alter_column(
            'resolution_status',
            existing_type=sa.String(length=30),
            type_=sa.Enum('UNRESOLVED', 'VISITOR', 'EMPLOYEE_CORRECTION', 'DISMISSED', 'SECURITY_REVIEW', name='unknownresolutionstatus', native_enum=False),
            nullable=False,
            server_default='UNRESOLVED',
        )

    # 7. Update visitors status enum
    with op.batch_alter_table('visitors', schema=None) as batch_op:
        batch_op.alter_column(
            'status',
            existing_type=sa.String(length=30),
            type_=sa.Enum('EXPECTED', 'CHECKED_IN', 'CHECKED_OUT', 'CANCELLED', name='visitorstatus', native_enum=False),
            nullable=False,
            server_default='EXPECTED',
        )

    # 8. Update manual_review_items status enum
    with op.batch_alter_table('manual_review_items', schema=None) as batch_op:
        batch_op.alter_column(
            'status',
            existing_type=sa.String(length=30),
            type_=sa.Enum('PENDING', 'APPROVED', 'REJECTED', 'RECLASSIFIED', name='reviewstatus', native_enum=False),
            nullable=False,
            server_default='PENDING',
        )

    # 9. Update system_events severity enum
    with op.batch_alter_table('system_events', schema=None) as batch_op:
        batch_op.alter_column(
            'severity',
            existing_type=sa.String(length=20),
            type_=sa.Enum('INFO', 'WARNING', 'ERROR', 'CRITICAL', name='eventseverity', native_enum=False),
            nullable=False,
            server_default='INFO',
        )


def downgrade() -> None:
    with op.batch_alter_table('system_events', schema=None) as batch_op:
        batch_op.alter_column(
            'severity',
            existing_type=sa.Enum('INFO', 'WARNING', 'ERROR', 'CRITICAL', name='eventseverity', native_enum=False),
            type_=sa.String(length=20),
            nullable=False,
            server_default='INFO',
        )

    with op.batch_alter_table('manual_review_items', schema=None) as batch_op:
        batch_op.alter_column(
            'status',
            existing_type=sa.Enum('PENDING', 'APPROVED', 'REJECTED', 'RECLASSIFIED', name='reviewstatus', native_enum=False),
            type_=sa.String(length=30),
            nullable=False,
            server_default='PENDING',
        )

    with op.batch_alter_table('visitors', schema=None) as batch_op:
        batch_op.alter_column(
            'status',
            existing_type=sa.Enum('EXPECTED', 'CHECKED_IN', 'CHECKED_OUT', 'CANCELLED', name='visitorstatus', native_enum=False),
            type_=sa.String(length=30),
            nullable=False,
            server_default='EXPECTED',
        )

    with op.batch_alter_table('unknown_people', schema=None) as batch_op:
        batch_op.alter_column(
            'resolution_status',
            existing_type=sa.Enum('UNRESOLVED', 'VISITOR', 'EMPLOYEE_CORRECTION', 'DISMISSED', 'SECURITY_REVIEW', name='unknownresolutionstatus', native_enum=False),
            type_=sa.String(length=30),
            nullable=False,
            server_default='UNRESOLVED',
        )

    with op.batch_alter_table('activity_segments', schema=None) as batch_op:
        batch_op.alter_column(
            'activity_state',
            existing_type=sa.Enum('SITTING', 'STANDING', 'WALKING', 'UNKNOWN', name='activitystate', native_enum=False),
            type_=sa.String(length=30),
            nullable=False,
        )

    with op.batch_alter_table('presence_sessions', schema=None) as batch_op:
        batch_op.alter_column(
            'status',
            existing_type=sa.Enum('VISIBLE', 'TEMPORARILY_LOST', 'LEFT_MONITORED_ZONE', 'RETURNED', 'SESSION_CLOSED', name='presencestatus', native_enum=False),
            type_=sa.String(length=30),
            nullable=False,
            server_default='VISIBLE',
        )

    with op.batch_alter_table('identity_verifications', schema=None) as batch_op:
        batch_op.alter_column(
            'status',
            existing_type=sa.Enum('CANDIDATE', 'CONFIRMED', 'UNKNOWN', 'AMBIGUOUS', 'REJECTED', 'MANUAL_REVIEW', name='recognitionstatus', native_enum=False),
            type_=sa.String(length=30),
            nullable=False,
        )

    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.alter_column(
            'enrollment_status',
            existing_type=sa.Enum('PENDING', 'IN_PROGRESS', 'COMPLETE', 'FAILED', 'DISABLED', name='enrollmentstatus', native_enum=False),
            type_=sa.String(length=30),
            nullable=False,
            server_default='PENDING',
        )
        batch_op.alter_column(
            'status',
            existing_type=sa.Enum('ACTIVE', 'INACTIVE', 'DISABLED', name='employeestatus', native_enum=False),
            type_=sa.String(length=20),
            nullable=False,
            server_default='ACTIVE',
        )

    with op.batch_alter_table('cameras', schema=None) as batch_op:
        batch_op.drop_constraint('chk_camera_source_consistency', type_='check')
        batch_op.alter_column(
            'status',
            existing_type=sa.Enum('OFFLINE', 'CONNECTING', 'ONLINE', 'DEGRADED', 'ERROR', 'DISABLED', name='camerastatus', native_enum=False),
            type_=sa.String(length=20),
            nullable=False,
            server_default='OFFLINE',
        )
        batch_op.alter_column('rtsp_url', existing_type=sa.String(length=255), nullable=False)
        batch_op.drop_column('credential_ref')
        batch_op.drop_column('device_index')
        batch_op.drop_column('source_type')
