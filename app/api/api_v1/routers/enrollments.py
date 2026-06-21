from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db, require_admin, require_student
from app.schemas.enrollment import EnrollmentRead
from app.services import enrollment as enrollment_service

router = APIRouter()


@router.post("/{course_id}", response_model=EnrollmentRead, dependencies=[Depends(require_student)])
def enroll_in_course(course_id: int, current_user=Depends(get_current_active_user), db: Session = Depends(get_db)):
    return enrollment_service.enroll_student(db, current_user, course_id)


@router.delete("/{course_id}", response_model=EnrollmentRead, dependencies=[Depends(require_student)])
def deregister_from_course(course_id: int, current_user=Depends(get_current_active_user), db: Session = Depends(get_db)):
    return enrollment_service.deregister_student(db, current_user, course_id)


@router.get("", response_model=list[EnrollmentRead], dependencies=[Depends(require_admin)])
def read_enrollments(db: Session = Depends(get_db)):
    return enrollment_service.get_all_enrollments(db)


@router.get("/course/{course_id}", response_model=list[EnrollmentRead], dependencies=[Depends(require_admin)])
def read_course_enrollments(course_id: int, db: Session = Depends(get_db)):
    return enrollment_service.get_enrollments_by_course(db, course_id)


@router.delete("/{course_id}/users/{user_id}", response_model=EnrollmentRead, dependencies=[Depends(require_admin)])
def remove_student_from_course(course_id: int, user_id: int, db: Session = Depends(get_db)):
    return enrollment_service.remove_student_from_course(db, course_id, user_id)
