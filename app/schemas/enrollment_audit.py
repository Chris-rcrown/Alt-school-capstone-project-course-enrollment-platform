from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EnrollmentAuditLogRead(BaseModel):
    id: int
    action: str
    actor_user_id: int | None
    target_user_id: int | None
    course_id: int | None
    enrollment_id: int | None
    detail: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
