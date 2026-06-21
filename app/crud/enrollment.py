from datetime import datetime

from sqlalchemy.orm import Session

from app.models.enrollment import Enrollment
from app.models.course import Course


def get_enrollment_by_user_course(db: Session, user_id: int, course_id: int) -> Enrollment | None:
    return (
        db.query(Enrollment)
        .filter(Enrollment.user_id == user_id, Enrollment.course_id == course_id)
        .first()
    )


def count_course_enrollments(db: Session, course_id: int) -> int:
    return db.query(Enrollment).filter(Enrollment.course_id == course_id).count()


def create_enrollment(db: Session, user_id: int, course_id: int) -> Enrollment:
    enrollment = Enrollment(user_id=user_id, course_id=course_id)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment


def delete_enrollment(db: Session, enrollment: Enrollment) -> None:
    db.delete(enrollment)
    db.commit()


def get_all_enrollments(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 20,
    user_id: int | None = None,
    course_id: int | None = None,
    created_from: datetime | None = None,
    created_to: datetime | None = None,
) -> list[Enrollment]:
    query = db.query(Enrollment)
    if user_id is not None:
        query = query.filter(Enrollment.user_id == user_id)
    if course_id is not None:
        query = query.filter(Enrollment.course_id == course_id)
    if created_from is not None:
        query = query.filter(Enrollment.created_at >= created_from)
    if created_to is not None:
        query = query.filter(Enrollment.created_at <= created_to)
    return query.order_by(Enrollment.created_at.desc()).offset(skip).limit(limit).all()


def get_enrollments_by_course(
    db: Session,
    course_id: int,
    *,
    skip: int = 0,
    limit: int = 20,
    user_id: int | None = None,
    created_from: datetime | None = None,
    created_to: datetime | None = None,
) -> list[Enrollment]:
    query = db.query(Enrollment).filter(Enrollment.course_id == course_id)
    if user_id is not None:
        query = query.filter(Enrollment.user_id == user_id)
    if created_from is not None:
        query = query.filter(Enrollment.created_at >= created_from)
    if created_to is not None:
        query = query.filter(Enrollment.created_at <= created_to)
    return query.order_by(Enrollment.created_at.desc()).offset(skip).limit(limit).all()
