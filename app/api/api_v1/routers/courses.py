from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_admin
from app.schemas.course import CourseCreate, CourseRead, CourseUpdate
from app.services import course as course_service

router = APIRouter()


@router.get("", response_model=list[CourseRead])
def list_active_courses(
    db: Session = Depends(get_db),
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    title: str | None = None,
    code: str | None = None,
    min_capacity: Annotated[int | None, Query(ge=1)] = None,
    max_capacity: Annotated[int | None, Query(ge=1)] = None,
):
    return course_service.get_courses(
        db,
        skip=skip,
        limit=limit,
        title=title,
        code=code,
        min_capacity=min_capacity,
        max_capacity=max_capacity,
    )


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


@router.delete("/{course_id}", response_model=CourseRead, dependencies=[Depends(require_admin)])
def delete_course(course_id: int, db: Session = Depends(get_db)):
    return course_service.soft_delete_course(db, course_id)
