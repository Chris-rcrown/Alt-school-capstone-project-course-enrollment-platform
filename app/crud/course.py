from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate


def get_course(db: Session, course_id: int) -> Course | None:
    return (
        db.query(Course)
        .filter(Course.id == course_id, Course.deleted_at.is_(None))
        .first()
    )


def get_course_by_code(db: Session, code: str) -> Course | None:
    return db.query(Course).filter(Course.code == code).first()


def get_active_courses(db: Session) -> list[Course]:
    return (
        db.query(Course)
        .filter(Course.is_active.is_(True), Course.deleted_at.is_(None))
        .all()
    )


def get_courses(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 20,
    title: str | None = None,
    code: str | None = None,
    min_capacity: int | None = None,
    max_capacity: int | None = None,
    is_active: bool | None = True,
) -> list[Course]:
    query = db.query(Course).filter(Course.deleted_at.is_(None))
    if is_active is not None:
        query = query.filter(Course.is_active.is_(is_active))
    if title:
        query = query.filter(Course.title.ilike(f"%{title}%"))
    if code:
        query = query.filter(Course.code.ilike(f"%{code}%"))
    if min_capacity is not None:
        query = query.filter(Course.capacity >= min_capacity)
    if max_capacity is not None:
        query = query.filter(Course.capacity <= max_capacity)
    return query.order_by(Course.id.asc()).offset(skip).limit(limit).all()


def create_course(db: Session, course_in: CourseCreate) -> Course:
    course = Course(
        title=course_in.title,
        code=course_in.code,
        capacity=course_in.capacity,
        is_active=True,
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def update_course(db: Session, course: Course, course_in: CourseUpdate) -> Course:
    if course_in.title is not None:
        course.title = course_in.title
    if course_in.code is not None:
        course.code = course_in.code
    if course_in.capacity is not None:
        course.capacity = course_in.capacity
    if course_in.is_active is not None:
        course.is_active = course_in.is_active
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def soft_delete_course(db: Session, course: Course) -> Course:
    course.is_active = False
    course.deleted_at = datetime.now(UTC)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course
