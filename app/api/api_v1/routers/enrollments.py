from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db, require_admin, require_student
from app.schemas.enrollment_audit import EnrollmentAuditLogRead
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
def read_enrollments(
    db: Session = Depends(get_db),
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    user_id: int | None = None,
    course_id: int | None = None,
    created_from: datetime | None = None,
    created_to: datetime | None = None,
):
    return enrollment_service.get_all_enrollments(
        db,
        skip=skip,
        limit=limit,
        user_id=user_id,
        course_id=course_id,
        created_from=created_from,
        created_to=created_to,
    )


@router.get("/course/{course_id}", response_model=list[EnrollmentRead], dependencies=[Depends(require_admin)])
def read_course_enrollments(
    course_id: int,
    db: Session = Depends(get_db),
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    user_id: int | None = None,
    created_from: datetime | None = None,
    created_to: datetime | None = None,
):
    return enrollment_service.get_enrollments_by_course(
        db,
        course_id,
        skip=skip,
        limit=limit,
        user_id=user_id,
        created_from=created_from,
        created_to=created_to,
    )


@router.delete("/{course_id}/users/{user_id}", response_model=EnrollmentRead, dependencies=[Depends(require_admin)])
def remove_student_from_course(
    course_id: int,
    user_id: int,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return enrollment_service.remove_student_from_course(db, course_id, user_id, actor_user_id=current_user.id)


@router.get("/audit-logs", response_model=list[EnrollmentAuditLogRead], dependencies=[Depends(require_admin)])
def read_enrollment_audit_logs(
    db: Session = Depends(get_db),
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    action: str | None = None,
    actor_user_id: int | None = None,
    target_user_id: int | None = None,
    course_id: int | None = None,
    created_from: datetime | None = None,
    created_to: datetime | None = None,
):
    return enrollment_service.get_enrollment_audit_logs(
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
