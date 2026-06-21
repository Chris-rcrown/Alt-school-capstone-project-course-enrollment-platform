from sqlalchemy.orm import Session

from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate


def get_course(db: Session, course_id: int) -> Course | None:
    return db.query(Course).filter(Course.id == course_id).first()


def get_course_by_code(db: Session, code: str) -> Course | None:
    return db.query(Course).filter(Course.code == code).first()


def get_active_courses(db: Session) -> list[Course]:
    return db.query(Course).filter(Course.is_active.is_(True)).all()


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
