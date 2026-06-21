from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_admin
from app.schemas.course import CourseCreate, CourseRead, CourseUpdate
from app.services import course as course_service

router = APIRouter()


@router.get("", response_model=list[CourseRead])
def list_active_courses(db: Session = Depends(get_db)):
    return course_service.get_active_courses(db)


@router.get("/{course_id}", response_model=CourseRead)
def read_course(course_id: int, db: Session = Depends(get_db)):
    course = course_service.get_course_by_id(db, course_id)
    return course


@router.post("", response_model=CourseRead, dependencies=[Depends(require_admin)])
def create_course(course_in: CourseCreate, db: Session = Depends(get_db)):
    return course_service.create_course(db, course_in)


@router.put("/{course_id}", response_model=CourseRead, dependencies=[Depends(require_admin)])
def update_course(course_id: int, course_in: CourseUpdate, db: Session = Depends(get_db)):
    return course_service.update_course(db, course_id, course_in)
