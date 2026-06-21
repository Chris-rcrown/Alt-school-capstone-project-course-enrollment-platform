from datetime import datetime

from sqlalchemy.orm import Session

from app.models.enrollment_audit_log import EnrollmentAuditLog


def create_audit_log(
    db: Session,
    *,
    action: str,
    actor_user_id: int | None,
    target_user_id: int | None,
    course_id: int | None,
    enrollment_id: int | None,
    detail: str | None = None,
) -> EnrollmentAuditLog:
    log = EnrollmentAuditLog(
        action=action,
        actor_user_id=actor_user_id,
        target_user_id=target_user_id,
        course_id=course_id,
        enrollment_id=enrollment_id,
        detail=detail,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def get_audit_logs(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 20,
    action: str | None = None,
    actor_user_id: int | None = None,
    target_user_id: int | None = None,
    course_id: int | None = None,
    created_from: datetime | None = None,
    created_to: datetime | None = None,
) -> list[EnrollmentAuditLog]:
    query = db.query(EnrollmentAuditLog)
    if action:
        query = query.filter(EnrollmentAuditLog.action == action)
    if actor_user_id is not None:
        query = query.filter(EnrollmentAuditLog.actor_user_id == actor_user_id)
    if target_user_id is not None:
        query = query.filter(EnrollmentAuditLog.target_user_id == target_user_id)
    if course_id is not None:
        query = query.filter(EnrollmentAuditLog.course_id == course_id)
    if created_from is not None:
        query = query.filter(EnrollmentAuditLog.created_at >= created_from)
    if created_to is not None:
        query = query.filter(EnrollmentAuditLog.created_at <= created_to)
    return (
        query.order_by(EnrollmentAuditLog.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
