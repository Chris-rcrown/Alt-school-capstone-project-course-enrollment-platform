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


def get_all_enrollments(db: Session) -> list[Enrollment]:
    return db.query(Enrollment).all()


def get_enrollments_by_course(db: Session, course_id: int) -> list[Enrollment]:
    return db.query(Enrollment).filter(Enrollment.course_id == course_id).all()
