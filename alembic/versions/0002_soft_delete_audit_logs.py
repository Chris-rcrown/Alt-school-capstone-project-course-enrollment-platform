"""Add soft deletes and enrollment audit logs

Revision ID: 0002_soft_delete_audit_logs
Revises: 0001_initial
Create Date: 2026-06-22 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "0002_soft_delete_audit_logs"
down_revision = "0001_initial"
branch_labels = None
depend_on = None


def upgrade():
    op.add_column("courses", sa.Column("deleted_at", sa.DateTime(), nullable=True))
    op.create_index(op.f("ix_courses_deleted_at"), "courses", ["deleted_at"], unique=False)

    op.create_table(
        "enrollment_audit_logs",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("action", sa.String(length=32), nullable=False),
        sa.Column("actor_user_id", sa.Integer(), nullable=True),
        sa.Column("target_user_id", sa.Integer(), nullable=True),
        sa.Column("course_id", sa.Integer(), nullable=True),
        sa.Column("enrollment_id", sa.Integer(), nullable=True),
        sa.Column("detail", sa.String(length=512), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["actor_user_id"], ["users.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["target_user_id"], ["users.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["course_id"], ["courses.id"], ondelete="SET NULL"),
    )
    op.create_index(op.f("ix_enrollment_audit_logs_action"), "enrollment_audit_logs", ["action"], unique=False)
    op.create_index(op.f("ix_enrollment_audit_logs_actor_user_id"), "enrollment_audit_logs", ["actor_user_id"], unique=False)
    op.create_index(op.f("ix_enrollment_audit_logs_target_user_id"), "enrollment_audit_logs", ["target_user_id"], unique=False)
    op.create_index(op.f("ix_enrollment_audit_logs_course_id"), "enrollment_audit_logs", ["course_id"], unique=False)
    op.create_index(op.f("ix_enrollment_audit_logs_enrollment_id"), "enrollment_audit_logs", ["enrollment_id"], unique=False)
    op.create_index(op.f("ix_enrollment_audit_logs_created_at"), "enrollment_audit_logs", ["created_at"], unique=False)


def downgrade():
    op.drop_index(op.f("ix_enrollment_audit_logs_created_at"), table_name="enrollment_audit_logs")
    op.drop_index(op.f("ix_enrollment_audit_logs_enrollment_id"), table_name="enrollment_audit_logs")
    op.drop_index(op.f("ix_enrollment_audit_logs_course_id"), table_name="enrollment_audit_logs")
    op.drop_index(op.f("ix_enrollment_audit_logs_target_user_id"), table_name="enrollment_audit_logs")
    op.drop_index(op.f("ix_enrollment_audit_logs_actor_user_id"), table_name="enrollment_audit_logs")
    op.drop_index(op.f("ix_enrollment_audit_logs_action"), table_name="enrollment_audit_logs")
    op.drop_table("enrollment_audit_logs")

    op.drop_index(op.f("ix_courses_deleted_at"), table_name="courses")
    op.drop_column("courses", "deleted_at")
