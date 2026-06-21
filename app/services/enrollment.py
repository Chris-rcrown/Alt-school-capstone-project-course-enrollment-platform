from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud import course as course_crud
from app.crud import enrollment_audit as enrollment_audit_crud
from app.crud import enrollment as enrollment_crud


def enroll_student(db: Session, user, course_id: int):
    course = course_crud.get_course(db, course_id)
    if not course or not course.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Course is not available for enrollment")
    if enrollment_crud.get_enrollment_by_user_course(db, user_id=user.id, course_id=course_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already enrolled in this course")
    seats_taken = enrollment_crud.count_course_enrollments(db, course_id)
    if seats_taken >= course.capacity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Course is full")
    enrollment = enrollment_crud.create_enrollment(db, user_id=user.id, course_id=course_id)
    enrollment_audit_crud.create_audit_log(
        db,
        action="enrolled",
        actor_user_id=user.id,
        target_user_id=user.id,
        course_id=course_id,
        enrollment_id=enrollment.id,
        detail="Student enrolled in course",
    )
    return enrollment


def deregister_student(db: Session, user, course_id: int):
    enrollment = enrollment_crud.get_enrollment_by_user_course(db, user_id=user.id, course_id=course_id)
    if not enrollment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")
    enrollment_id = enrollment.id
    enrollment_crud.delete_enrollment(db, enrollment)
    enrollment_audit_crud.create_audit_log(
        db,
        action="deregistered",
        actor_user_id=user.id,
        target_user_id=user.id,
        course_id=course_id,
        enrollment_id=enrollment_id,
        detail="Student deregistered from course",
    )
    return enrollment


def get_all_enrollments(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 20,
    user_id: int | None = None,
    course_id: int | None = None,
    created_from: datetime | None = None,
    created_to: datetime | None = None,
):
    return enrollment_crud.get_all_enrollments(
        db,
        skip=skip,
        limit=limit,
        user_id=user_id,
        course_id=course_id,
        created_from=created_from,
        created_to=created_to,
    )


def get_enrollments_by_course(
    db: Session,
    course_id: int,
    *,
    skip: int = 0,
    limit: int = 20,
    user_id: int | None = None,
    created_from: datetime | None = None,
    created_to: datetime | None = None,
):
    return enrollment_crud.get_enrollments_by_course(
        db,
        course_id,
        skip=skip,
        limit=limit,
        user_id=user_id,
        created_from=created_from,
        created_to=created_to,
    )


def remove_student_from_course(db: Session, course_id: int, user_id: int, *, actor_user_id: int | None = None):
    enrollment = enrollment_crud.get_enrollment_by_user_course(db, user_id=user_id, course_id=course_id)
    if not enrollment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")
    enrollment_id = enrollment.id
    enrollment_crud.delete_enrollment(db, enrollment)
    enrollment_audit_crud.create_audit_log(
        db,
        action="removed_by_admin",
        actor_user_id=actor_user_id,
        target_user_id=user_id,
        course_id=course_id,
        enrollment_id=enrollment_id,
        detail="Enrollment removed by admin",
    )
    return enrollment


def get_enrollment_audit_logs(
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
):
    return enrollment_audit_crud.get_audit_logs(
        db,
        skip=skip,
        limit=limit,
        action=action,
        actor_user_id=actor_user_id,
        target_user_id=target_user_id,
        course_id=course_id,
        created_from=created_from,
        created_to=created_to,
    )
