from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud import course as course_crud
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
    return enrollment_crud.create_enrollment(db, user_id=user.id, course_id=course_id)


def deregister_student(db: Session, user, course_id: int):
    enrollment = enrollment_crud.get_enrollment_by_user_course(db, user_id=user.id, course_id=course_id)
    if not enrollment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")
    enrollment_crud.delete_enrollment(db, enrollment)
    return enrollment


def get_all_enrollments(db: Session):
    return enrollment_crud.get_all_enrollments(db)


def get_enrollments_by_course(db: Session, course_id: int):
    return enrollment_crud.get_enrollments_by_course(db, course_id)


def remove_student_from_course(db: Session, course_id: int, user_id: int):
    enrollment = enrollment_crud.get_enrollment_by_user_course(db, user_id=user_id, course_id=course_id)
    if not enrollment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")
    enrollment_crud.delete_enrollment(db, enrollment)
    return enrollment
