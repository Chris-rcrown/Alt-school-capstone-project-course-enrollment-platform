from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud import course as course_crud
from app.schemas.course import CourseCreate, CourseUpdate


def create_course(db: Session, course_in: CourseCreate):
    existing_course = course_crud.get_course_by_code(db, course_in.code)
    if existing_course:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Course code must be unique")
    if course_in.capacity <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Capacity must be greater than zero")
    return course_crud.create_course(db, course_in)


def update_course(db: Session, course_id: int, course_in: CourseUpdate):
    course = course_crud.get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    if course_in.code is not None:
        existing_course = course_crud.get_course_by_code(db, course_in.code)
        if existing_course and existing_course.id != course.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Course code must be unique")
    if course_in.capacity is not None and course_in.capacity <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Capacity must be greater than zero")
    return course_crud.update_course(db, course, course_in)


def get_active_courses(db: Session):
    return course_crud.get_active_courses(db)


def get_course_by_id(db: Session, course_id: int):
    course = course_crud.get_course(db, course_id)
    if not course or not course.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course
